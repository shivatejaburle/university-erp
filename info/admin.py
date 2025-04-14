from django.contrib import admin
from info.models import User, Department, Class, Student, Course, Teacher, Assign, StudentCourse, AttendanceClass, AssignTime, Marks, AttendanceRange, Attendance, HOD
from datetime import timedelta, datetime
from django.urls import path
from django.http import HttpResponseRedirect

# Date Range
def dateRange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}

# Inlines

class ClassInline(admin.TabularInline):
    model = Class
    extra = 0

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

class AssignTimeInline(admin.TabularInline):
    model = AssignTime
    extra = 0

class MarksInline(admin.TabularInline):
    model = Marks
    extra = 0

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_student', 'is_teacher', 'is_hod')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ['name']
    inlines = [ClassInline]

class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'semester', 'section')
    search_fields = ('id', 'department__name', 'semester', 'section')
    ordering = ['department__name', 'semester', 'section']
    inlines = [StudentInline]

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'class_id')
    search_fields = ('roll_number', 'name', 'class_id__id', 'class_id__department__name')
    ordering = ['class_id__department__name', 'class_id__id', 'roll_number']

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'short_name')
    search_fields = ('id', 'name', 'department__name', 'short_name')
    ordering = ['department', 'id']

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name', 'department__name')
    ordering = ('department__name', 'name')

class AssignAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'course', 'teacher')
    search_fields = ('class_id__department__name', 'class_id__id', 'course__name', 'teacher__name', 'course__short_name')
    ordering = ('class_id__department__name', 'class_id__id', 'course__id')
    inlines = [AssignTimeInline]
    raw_id_fields = ['class_id', 'course', 'teacher']

class StudentCourseAdmin(admin.ModelAdmin):
    pass
    list_display = ('student', 'course')
    search_fields = ('student__name', 'course__name', 'student__class_id__id', 'student__class_id__department__name')
    ordering = ['student__class_id__department__name', 'student__class_id__id', 'student__roll_number']
    inlines = [MarksInline]

# Reset Attendance
class AttendanceClassAdmin(admin.ModelAdmin):
    list_display = ('assign', 'date', 'status')
    ordering = ['assign', 'date']
    change_list_template = 'info/admin/attendance/attendance_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('reset_attendance/', self.reset_attendance, name='reset_attendance'),
        ]
        return new_urls + urls
    
    def reset_attendance(self, request):
        start_date = datetime.strptime(request.POST['startDate'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['endDate'], '%Y-%m-%d').date()

        try:
            attendance = AttendanceRange.objects.all()[:1].get()
            attendance.start_date = start_date
            attendance.end_date = end_date
            attendance.save()
        except AttendanceRange.DoesNotExist:
            attendance = AttendanceRange(start_date=start_date, end_date=end_date)
            attendance.save()

        Attendance.objects.all().delete()
        AttendanceClass.objects.all().delete()

        for assign_time in AssignTime.objects.all():
            for single_date in dateRange(start_date, end_date):
                if single_date.isoweekday() == days[assign_time.day]:
                    try:
                        AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=assign_time.assign)
                    except AttendanceClass.DoesNotExist:
                        attendance = AttendanceClass.objects.create(date=single_date.strftime("%Y-%m-%d"), assign=assign_time.assign)
                        attendance.save()
        
        self.message_user(request, "Attendance Dates Reset Successfully.")
        return HttpResponseRedirect("../")

admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assign, AssignAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(AttendanceClass, AttendanceClassAdmin)
admin.site.register(HOD)