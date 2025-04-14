from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, RedirectView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from info.models import User, Department, Course, Class, Teacher, Assign, AssignTime, Student, AttendanceClass, Attendance, AttendanceTotal, MarksClass, StudentCourse, days_of_week, time_slots, Marks, AttendanceRange, HOD
from django.contrib import messages
from info.forms import AdminForm, DepartmentForm, CourseForm, ClassForm, TeacherForm, StudentForm, HODForm
from info.forms import DepartmentClassFormset, ClassStudentFormset, AssignTimeFormset, StudentCourseMarksFormset
from allauth.account.models import EmailAddress
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views.generic.detail import SingleObjectMixin
from datetime import datetime
from info.admin import dateRange, days

# Index View
class IndexView(TemplateView):
    template_name = 'info/index.html'

# Unauthorize View
class UnauthorizeView(TemplateView):
    template_name = 'info/unauthorize.html'

# Check the user type and redirect to respective dashboard
def login_success(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('info:admin_view')
        elif request.user.is_teacher:
            return redirect('info:teacher_view')
        elif request.user.is_student:
            return redirect('info:student_view')
        else:
            return render(request, 'info/index.html')
    return render(request, 'info/index.html')

# ================== Dashboards ================== #

# Admin Dashboard View
class AdminView(LoginRequiredMixin, TemplateView):
    template_name = 'info/admin/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# Teacher Dashboard View
class TeacherView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# Student Dashboard View
class StudentView(LoginRequiredMixin, TemplateView):
    template_name = 'info/student/index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# HOD Dashboard View
class HODView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# ================== Admin Views ================== #

# Create Admin User
class CreateAdminUser(LoginRequiredMixin, CreateView):
    model = User
    # fields = ['username', 'email', 'is_superuser']
    form_class = AdminForm
    template_name = 'info/admin/create_admin_user.html'
    success_url = reverse_lazy('info:admin_view')
    
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = AdminForm()
            context = context = {
                'form':form
            }
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        form = AdminForm(request.POST)
        if not form.is_valid():
            context = {
                'form':form
            }
            return render(request, self.template_name, context)
        
        obj = request.POST
        # Create Admin User in User Model
        new_admin_user = User.objects.create_superuser(username=obj['username'], email=obj['email'], password=obj['password'])
        # EmailAddress for Django Allauth
        EmailAddress.objects.create(user=new_admin_user, email=new_admin_user.email, primary=True, verified=False)
        
        messages.success(request, "Admin User was successfully created.")
        return redirect(self.success_url)
    
# Manage Data Navigation View
class ManageData(LoginRequiredMixin, TemplateView):
    template_name = 'info/admin/manage_data.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ManageData, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['department_list'] = Department.objects.all()
        context['course_list'] = Course.objects.all()
        context['class_list'] = Class.objects.all()
        context['student_list'] = Student.objects.all()
        context['teacher_list'] = Teacher.objects.all()
        context['assign_list'] = Assign.objects.all()
        context['assign_time_list'] = AssignTime.objects.all()
        context['marks_list'] = StudentCourse.objects.all()
        context['attendance_range_list'] = AttendanceRange.objects.all()
        context['hod_list'] = HOD.objects.all()
        return context

# Create Department
class CreateDepartment(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'info/admin/department_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Department was successfully created."

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Update Department
class UpdateDepartment(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Department
    fields = ['name']
    template_name = 'info/admin/department_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Department was successfully updated."
    context_object_name = 'department'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

     # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UpdateDepartment, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context
    
# Delete Department
class DeleteDepartment(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Department
    template_name = 'info/admin/department_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Department was successfully deleted."
    context_object_name = 'department'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Create Course
class CreateCourse(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'info/admin/course_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Course was successfully created."

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Update Course
class UpdateCourse(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ['department', 'name', 'short_name']
    template_name = 'info/admin/course_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Course was successfully updated."
    context_object_name = 'course'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not (request.user.is_superuser or request.user.is_hod):
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

     # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UpdateCourse, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context
    
# Delete Course
class DeleteCourse(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Course
    template_name = 'info/admin/course_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Course was successfully deleted."
    context_object_name = 'course'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Create Class
class CreateClass(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'info/admin/class_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Class was successfully created."

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Update Class
class UpdateClass(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Class
    fields = ['department', 'section', 'semester']
    template_name = 'info/admin/class_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Class was successfully updated."
    context_object_name = 'class'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UpdateClass, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context
    
# Delete Class
class DeleteClass(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Class
    template_name = 'info/admin/class_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Class was successfully deleted."
    context_object_name = 'class'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Create Teacher
class CreateTeacher(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'info/admin/teacher_form.html'
    success_url = reverse_lazy('info:manage_data_nav')

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = TeacherForm()
            context = context = {
                'form':form
            }
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        form = TeacherForm(request.POST)
        if not form.is_valid():
            context = {
                'form':form
            }
            return render(request, self.template_name, context)
        
        # Get all form data
        obj = request.POST
        
        # USERNAME: firstname + underscore + unique ID
        username = obj['name'].split(" ")[0].lower() + '_' + obj['teacher_id'].lower()

        # PASSWORD: firstname + underscore + year of birth(YYYY)
        password = obj['name'].split(" ")[0].lower() + '_' + obj['date_of_birth'].replace('-', '')[:4]

        # Create Teacher in User Model
        new_user = User.objects.create_user(username=username, email=obj['email_address'], password=password, is_teacher=True)
        
        # EmailAddress for Django Allauth
        EmailAddress.objects.create(user=new_user, email=new_user.email, primary=True, verified=False)
        
        # Create Teacher in Teacher Model
        department = get_object_or_404(Department, id=obj['department'])
        Teacher.objects.create(user=new_user, teacher_id=obj['teacher_id'], department=department, name=obj['name'], gender=obj['gender'], date_of_birth=obj['date_of_birth'])

        messages.success(request, "Teacher was successfully created.")
        return redirect(self.success_url)
    
# Update Teacher
class UpdateTeacher(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Teacher
    fields = ['name', 'gender', 'department']
    template_name = 'info/admin/teacher_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Teacher was successfully updated."
    context_object_name = 'teacher'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UpdateTeacher, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context

# Delete Teacher
class DeleteTeacher(LoginRequiredMixin, DeleteView):
    model = Teacher
    fields = ['name', 'gender', 'department']
    template_name = 'info/admin/teacher_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    context_object_name = 'teacher'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        teacher = User.objects.get(username=self.object.user.username)
        teacher.delete()
        messages.success(request, "Teacher was successfully deleted.")
        return redirect(self.success_url)

# Assign HOD
class AssignHOD(LoginRequiredMixin, CreateView):
    model = HOD
    form_class = HODForm
    template_name = 'info/admin/hod_form.html'
    success_url = reverse_lazy('info:manage_data_nav')

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = HODForm(request.POST)
        if not form.is_valid():
            context = {
                'form':form
            }
            return render(request, self.template_name, context)
        self.object = form.save(commit=True)
        teacher = User.objects.get(username=self.object.name.user.username)
        teacher.is_hod = True
        teacher.save()
        messages.success(request, "HOD was successfully assigned.")
        return redirect(self.success_url)

# Unassign HOD
class UnassignHOD(LoginRequiredMixin, DeleteView):
    model = HOD
    template_name = 'info/admin/hod_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    context_object_name = 'hod'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        teacher = User.objects.get(username=self.object.name.user.username)
        teacher.is_hod = False
        teacher.save()
        self.object.delete()
        messages.success(request, "HOD was successfully unassigned.")
        return redirect(self.success_url)

# Assign Teacher to Class and Course
class CreateAssign(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Assign
    fields = ['teacher', 'class_id', 'course']
    template_name = 'info/admin/assign_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Teacher was successfully assigned to Class and Course."
    context_object_name = 'assign'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Update Assign
class UpdateAssign(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Assign
    fields = ['teacher', 'class_id', 'course']
    template_name = 'info/admin/assign_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Teacher was successfully updated."
    context_object_name = 'assign'
    pk_url_kwarg = 'pk'

    # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UpdateAssign, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Delete Assign
class DeleteAssign(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Assign
    template_name = 'info/admin/assign_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Teacher was successfully unassigned from Class and Course."
    context_object_name = 'assign'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Assign Time Slots
class AssignTimeSlots(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssignTime
    fields = ['assign', 'period', 'day']
    template_name = 'info/admin/assign_time_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Time slots were successfully assigned."
    context_object_name = 'assign_time'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Delete Time Slots
class DeleteTimeSlots(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AssignTime
    template_name = 'info/admin/assign_time_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Time slots were successfully deleted."
    context_object_name = 'assign_time'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    

# Create Student
class CreateStudent(LoginRequiredMixin, CreateView):
    model = Student
    form_class = AdminForm
    template_name = 'info/admin/student_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = StudentForm()
            context = context = {
                'form':form
            }
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        if not form.is_valid():
            context = {
                'form':form
            }
            return render(request, self.template_name, context)
        
        # Get all form data
        obj = request.POST
        
        # USERNAME: firstname + underscore + last 3 digits of Roll Number
        username = obj['name'].split(" ")[0].lower() + '_' + obj['roll_number'][-3:]

        # PASSWORD: firstname + underscore + year of birth(YYYY)
        password = obj['name'].split(" ")[0].lower() + '_' + obj['date_of_birth'].replace('-', '')[:4]

        # Create Student in User Model
        new_user = User.objects.create_user(username=username, email=obj['email_address'], password=password, is_student=True)
        
        # EmailAddress for Django Allauth
        EmailAddress.objects.create(user=new_user, email=new_user.email, primary=True, verified=False)
        
        # Create Student in Student Model
        class_id = get_object_or_404(Class, id=obj['class_id'])
        Student.objects.create(user=new_user, class_id=class_id, roll_number=obj['roll_number'], name=obj['name'], gender=obj['gender'], date_of_birth=obj['date_of_birth'])

        messages.success(request, "Student was successfully created.")
        return redirect(self.success_url)
    
# Update Student
class UpdateStudent(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = ['name', 'gender', 'date_of_birth', 'class_id']
    template_name = 'info/admin/student_form.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Student was successfully updated."
    context_object_name = 'student'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UpdateStudent, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context
    
# Delete Student
class DeleteStudent(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Student
    template_name = 'info/admin/student_confirm_delete.html'
    success_url = reverse_lazy('info:manage_data_nav')
    success_message = "Student was successfully deleted."
    context_object_name = 'student'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        student = User.objects.get(username=self.object.user.username)
        student.delete()
        messages.success(request, "Student was successfully deleted.")
        return redirect(self.success_url)

class AttendanceRangeView(LoginRequiredMixin, TemplateView):
    template_name = 'info/admin/attendance_range.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

    def post(self, request, *args, **kwargs):
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        
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
        
        messages.success(request, "Attendance Dates Reset Successfully.")
        return redirect('info:manage_data_nav')

# ================== Teacher Views ================== #

# Teacher Classes View
class TeacherClassView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/class_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            teacher = get_object_or_404(Teacher, teacher_id=request.user.teacher.teacher_id)
            context['teacher'] = teacher
            context['choice'] = 1
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Teacher Class Dates
class TeacherClassDatesView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/class_dates.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            now = timezone.now()
            assign_id = kwargs['assign_id']
            assign = get_object_or_404(Assign, id=assign_id)
            attendance_list = assign.attendanceclass_set.filter(date__lte=now).order_by('-date')
            context['attendance_list'] = attendance_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Teacher Attendance View
class TeacherAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/attendance.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            assign_class_id = kwargs['assign_class_id']
            assign_class = get_object_or_404(AttendanceClass, id=assign_class_id)
            assign = assign_class.assign
            class_id = assign.class_id
            context['assign'] = assign
            context['class'] = class_id
            context['assign_class'] = assign_class
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        assign_class_id = kwargs['assign_class_id']
        assign_class = get_object_or_404(AttendanceClass, id=assign_class_id)
        assign = assign_class.assign
        course = assign.course
        class_id = assign.class_id

        for i, student, in enumerate(class_id.student_set.all()):
            status = request.POST[student.roll_number]
            if status == 'present':
                status = 'True'
            else:
                status = 'False'

            if assign_class.status == 1:
                try:
                    attendance = Attendance.objects.get(course = course, student = student, date = assign_class.date, attendanceClass = assign_class)
                    attendance.status = status
                    attendance.save()
                except Attendance.DoesNotExist:
                    attendance = Attendance(course = course, student = student, date = assign_class.date, attendanceClass = assign_class, status=status)
                    attendance.save()
            else:
                attendance = Attendance(course = course, student = student, status=status, date = assign_class.date, attendanceClass = assign_class)
                attendance.save()
                assign_class.status = 1
                assign_class.save()

        messages.success(request, "Successfully submitted the Attendance.")
        return HttpResponseRedirect(reverse_lazy('info:teacher_class_detail_view', kwargs={'assign_id': assign.id}))
    
# Cancel Class
class CancelClassView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        assign_class_id = kwargs['assign_class_id']
        assign_class = get_object_or_404(AttendanceClass, id=assign_class_id)
        assign_class.status = 2
        assign_class.save()
        messages.warning(request, "Successfully cancelled the Class.")
        return HttpResponseRedirect(reverse_lazy('info:teacher_class_detail_view', kwargs={'assign_id': assign_class.assign_id}))
    
# Edit Attendance
class EditAttendance(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/edit_attendance.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            assign_class_id = kwargs['assign_class_id']
            assign_class = get_object_or_404(AttendanceClass, id=assign_class_id)
            course = assign_class.assign.course
            attendance_list = Attendance.objects.filter(attendanceClass = assign_class, course = course)
            context['assign_class'] = assign_class
            context['attendance_list'] = attendance_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        assign_class_id = kwargs['assign_class_id']
        assign_class = get_object_or_404(AttendanceClass, id=assign_class_id)
        assign = assign_class.assign
        course = assign.course
        class_id = assign.class_id

        for i, student, in enumerate(class_id.student_set.all()):
            status = request.POST[student.roll_number]
            if status == 'present':
                status = 'True'
            else:
                status = 'False'

            if assign_class.status == 1:
                try:
                    attendance = Attendance.objects.get(course = course, student = student, date = assign_class.date, attendanceClass = assign_class)
                    attendance.status = status
                    attendance.save()
                except Attendance.DoesNotExist:
                    attendance = Attendance(course = course, student = student, date = assign_class.date, attendanceClass = assign_class, status=status)
                    attendance.save()
            else:
                attendance = Attendance(course = course, student = student, status=status, date = assign_class.date, attendanceClass = assign_class)
                attendance.save()
                assign_class.status = 1
                assign_class.save()

        messages.success(request, "Successfully updated the Attendance.")
        return HttpResponseRedirect(reverse_lazy('info:teacher_class_detail_view', kwargs={'assign_id': assign.id}))

# Extra Class
class ExtraClass(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/extra_class.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            assign_id = kwargs['assign_id']
            assign = get_object_or_404(Assign, id=assign_id)
            class_id = assign.class_id
            context['assign'] = assign
            context['class'] = class_id
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        assign_id = kwargs['assign_id']
        assign = get_object_or_404(Assign, id=assign_id)
        class_id = assign.class_id
        course = assign.course
        assign_class = assign.attendanceclass_set.create(status=1, date=request.POST['date'])
        assign_class.save()

        for i, student in enumerate(class_id.student_set.all()):
            status = request.POST[student.roll_number]
            if status == 'present':
                status = 'True'
            else:
                status = 'False'
            date = request.POST['date']
            attendance = Attendance(course=course, student=student, date=date, attendanceClass=assign_class)
            attendance.save()
        messages.success(request, "Successfully submitted attendance for extra class.")
        return redirect(reverse_lazy('info:teacher_class_view'))
    
# View Students
class ViewStudents(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/view_students.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            assign_id = kwargs['assign_id']
            assign = Assign.objects.get(id=assign_id)
            attendance_list = []
            for student in assign.class_id.student_set.all():
                try:
                    attendance = AttendanceTotal.objects.get(student=student, course=assign.course)
                except AttendanceTotal.DoesNotExist:
                    attendance = AttendanceTotal(student=student, course=assign.course)
                    attendance.save()
                attendance_list.append(attendance)
            context['attendance_list'] = attendance_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Attendance Detail View
class AttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/attendance_detail.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            roll_number = kwargs['roll_number']
            course_id = kwargs['course_id']
            student = get_object_or_404(Student, roll_number=roll_number)
            course = get_object_or_404(Course, id=course_id)
            attendance_list = Attendance.objects.filter(course=course, student=student).order_by('date')
            context['attendance_list'] = attendance_list
            context['course'] = course
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Change Attendance
class ChangeAttendance(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        attendance_id = kwargs['attendance_id']
        attendance = get_object_or_404(Attendance, id=attendance_id)
        attendance.status = not attendance.status
        attendance.save()
        return HttpResponseRedirect(reverse_lazy('info:attendance_detail_view', kwargs={'roll_number': attendance.student.roll_number, 'course_id': attendance.course_id}))

# Teacher Marks View
class TeacherViewMarks(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/class_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            teacher = get_object_or_404(Teacher, teacher_id=request.user.teacher.teacher_id)
            context['teacher'] = teacher
            context['choice'] = 2
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Teacher Marks List
class TeacherMarksListView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/marks_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            assign_id = kwargs['assign_id']
            assign = get_object_or_404(Assign, id=assign_id)
            marks_list = MarksClass.objects.filter(assign=assign_id)
            context['marks_list'] = marks_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# Teacher Marks Entry
class TeacherMarksEntryView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/marks_entry.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            marks_class_id = kwargs['marks_class_id']
            marks_class = get_object_or_404(MarksClass, id=marks_class_id)
            assign = marks_class.assign
            class_id = assign.class_id
            context['marks_class'] = marks_class
            context['assign'] = assign
            context['class'] = class_id
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        marks_class_id = kwargs['marks_class_id']
        marks_class = get_object_or_404(MarksClass, id=marks_class_id)
        assign = marks_class.assign
        course = assign.course
        class_id = assign.class_id
        for student in class_id.student_set.all():
            marks_gained = request.POST[student.roll_number]
            student_course = StudentCourse.objects.get(course=course, student=student)

            try:
                student_course.marks_set.get(name = marks_class.name)
            except:
                student_course.marks_set.create(name = marks_class.name)

            student_marks = student_course.marks_set.get(name = marks_class.name)
            student_marks.marks1 = marks_gained
            student_marks.save()
        marks_class.status = True
        marks_class.save()
        messages.success(request, "Successfully submitted the marks.")
        return HttpResponseRedirect(reverse_lazy('info:teacher_marks_view', kwargs={'assign_id': assign.id}))
    
# Teacher Edit Marks
class TeacherEditMarksView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/edit_marks.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            marks_class_id = kwargs['marks_class_id']
            marks_class = get_object_or_404(MarksClass, id=marks_class_id)
            course = marks_class.assign.course
            student_list = marks_class.assign.class_id.student_set.all()
            marks_list = []
            for student in student_list:
                student_course = StudentCourse.objects.get(course=course, student=student)
                
                try:
                    student_course.marks_set.get(name = marks_class.name)
                except:
                    student_course.marks_set.create(name = marks_class.name)
                
                marks = student_course.marks_set.get(name = marks_class.name)
                marks_list.append(marks)

            context['marks_class'] = marks_class
            context['marks_list'] = marks_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def post(self, request, *args, **kwargs):
        marks_class_id = kwargs['marks_class_id']
        marks_class = get_object_or_404(MarksClass, id=marks_class_id)
        assign = marks_class.assign
        course = assign.course
        class_id = assign.class_id
        for student in class_id.student_set.all():
            marks_gained = request.POST[student.roll_number]
            student_course = StudentCourse.objects.get(course=course, student=student)
            student_marks = student_course.marks_set.get(name = marks_class.name)
            student_marks.marks1 = marks_gained
            student_marks.save()
        marks_class.status = True
        marks_class.save()
        messages.success(request, "Successfully updated the marks.")
        return HttpResponseRedirect(reverse_lazy('info:teacher_marks_view', kwargs={'assign_id': assign.id}))
    
# Teacher View Student Marks
class TeacherViewStudentMarks(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/student_marks.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            assign_id = kwargs['assign_id']
            assign = Assign.objects.get(id = assign_id)
            student_course_list = StudentCourse.objects.filter(student__in=assign.class_id.student_set.all(), course=assign.course)
            context['student_course_list'] = student_course_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Teacher Timetable
class TeacherTimetable(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/timetable.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            teacher_id = kwargs['teacher_id']
            assign_time = AssignTime.objects.filter(assign__teacher_id=teacher_id)
            class_matrix = [[True for period in range(12)] for day in range(6)]
            for row, day in enumerate(days_of_week):
                t = 0
                for col in range(12):
                    if col == 0:
                        class_matrix[row][0] = day[0]
                        continue
                    if col == 4 or col == 8:
                        continue
                    try:
                        a = assign_time.get(period=time_slots[t][0], day=day[0])
                        class_matrix[row][col] = a
                    except AssignTime.DoesNotExist:
                        pass
                    t += 1
            
            context['timetable'] = class_matrix
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Free Teachers
class FreeTeachers(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/free_teachers.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            assign_time_id = kwargs['assign_time_id']
            assign_time = get_object_or_404(AssignTime, id=assign_time_id)
            free_teachers_list = []
            teachers_list = Teacher.objects.filter(assign__class_id__id=assign_time.assign.class_id_id)
            for teacher in teachers_list:
                assign_time_list = AssignTime.objects.filter(assign__teacher=teacher)
                if not any([True if at.period == assign_time.period and at.day == assign_time.day else False for at in assign_time_list ]):
                    free_teachers_list.append(teacher)
            context['free_teachers_list'] = free_teachers_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# Teacher Reports View 
class TeacherReportClassesView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/class_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            teacher = get_object_or_404(Teacher, teacher_id=request.user.teacher.teacher_id)
            context['teacher'] = teacher
            context['choice'] = 3
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Teacher Generate Report
class TeacherReportView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/teacher_report.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            assign_id = kwargs['assign_id']
            assign = get_object_or_404(Assign, id=assign_id)
            student_course_list = []
            for student in assign.class_id.student_set.all():
                try:
                    student_course = StudentCourse.objects.get(student=student, course=assign.course)
                except StudentCourse.DoesNotExist:
                    student_course = StudentCourse.objects.create(student=student, course=assign.course)
                    student_course.save()
                obj = StudentCourse.objects.get(student=student, course=assign.course)
                student_course_list.append(obj)
            context['student_course_list'] = student_course_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# ================== Student Views ================== #

# Student Attendance
class StudentAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'info/student/attendance.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            context = self.get_context_data(**kwargs)
            roll_number = kwargs['roll_number']
            student = Student.objects.get(roll_number=roll_number)
            assign_list = Assign.objects.filter(class_id_id=student.class_id)
            attendance_list = []
            for assign in assign_list:
                try:
                    attendance = AttendanceTotal.objects.get(student=student, course=assign.course)
                except AttendanceTotal.DoesNotExist:
                    attendance = AttendanceTotal(student=student, course=assign.course)
                    attendance.save()
                attendance_list.append(attendance)
            context['attendance_list'] = attendance_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# Student Attendance Details
class StudentAttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'info/student/attendance_detail.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            context = self.get_context_data(**kwargs)
            roll_number = kwargs['roll_number']
            course_id = kwargs['course_id']
            student = get_object_or_404(Student, roll_number=roll_number)
            course = get_object_or_404(Course, id=course_id)
            attendance_list = Attendance.objects.filter(course=course, student=student).order_by('date')
            context['attendance_list'] = attendance_list
            context['course'] = course
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Student Marks View
class StudentMarksListView(LoginRequiredMixin, TemplateView):
    template_name = 'info/student/marks_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            context = self.get_context_data(**kwargs)
            roll_number = kwargs['roll_number']
            student = Student.objects.get(roll_number=roll_number)
            assign_list = Assign.objects.filter(class_id_id=student.class_id)
            student_course_list = []
            for assign in assign_list:
                try:
                    student_course = StudentCourse.objects.get(student=student, course=assign.course)
                except:
                    student_course = StudentCourse(student=student, course=assign.course)
                    student_course.save()
                    student_course.marks_set.create(name = 'Midterm 1')
                    student_course.marks_set.create(name = 'Midterm 2')
                    student_course.marks_set.create(name = 'Midterm 3')
                    student_course.marks_set.create(name = 'Event 1')
                    student_course.marks_set.create(name = 'Event 2')
                    student_course.marks_set.create(name = 'Semester Final Exam')
                student_course_list.append(student_course)
            context['student_course_list'] = student_course_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Student Timetable
class StudentTimetable(LoginRequiredMixin, TemplateView):
    template_name = 'info/student/timetable.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            context = self.get_context_data(**kwargs)
            class_id = kwargs['class_id']
            assign_time = AssignTime.objects.filter(assign__class_id=class_id)
            class_matrix = [['' for period in range(12)] for day in range(6)]
            for row, day in enumerate(days_of_week):
                t = 0
                for col in range(12):
                    if col == 0:
                        class_matrix[row][0] = day[0]
                        continue
                    if col == 4 or col == 8:
                        continue
                    try:
                        a = assign_time.get(period=time_slots[t][0], day=day[0])
                        class_matrix[row][col] = a.assign.course_id
                    except AssignTime.DoesNotExist:
                        pass
                    t += 1
            
            context['timetable'] = class_matrix
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# ================== HOD Views ================== #

# Manage Department
class ManageDepartment(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/manage_dept.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ManageDepartment, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['hod_list'] = HOD.objects.all()
        context['course_list'] = Course.objects.filter(department_id=self.request.user.teacher.department_id)
        context['class_list'] = Class.objects.filter(department_id=self.request.user.teacher.department_id)
        context['teacher_list'] = Teacher.objects.filter(department_id=self.request.user.teacher.department_id)
        context['assign_list'] = Assign.objects.filter(class_id__department=self.request.user.teacher.department_id)
        context['assign_time_list'] = AssignTime.objects.filter(assign__class_id__department=self.request.user.teacher.department_id)
        context['student_list'] = Student.objects.filter(class_id__department_id=self.request.user.teacher.department_id)
        return context
    
# Courses in the Department
class DepartmentCourses(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/dept_courses.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def get_context_data(self, **kwargs):
        context = super(DepartmentCourses, self).get_context_data(**kwargs)
        context['course_list'] = Course.objects.filter(department_id=self.request.user.teacher.department_id)
        return context
    
# HOD Create Course
class HodCreateCourse(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['id', 'name', 'short_name']
    template_name = 'info/hod/course_form.html'
    success_url = reverse_lazy('info:department_courses')

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        obj = request.POST
        Course.objects.create(
            id=obj['id'],
            name=obj['name'], 
            short_name=obj['short_name'], 
            department_id=self.request.user.teacher.department_id
        ).save()
        messages.success(request, "Course was successfully created.")
        return redirect(self.success_url)
    
# HOD Update Course
class HodUpdateCourse(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    fields = ['name', 'short_name']
    template_name = 'info/hod/course_form.html'
    success_url = reverse_lazy('info:department_courses')
    success_message = "Course was successfully updated."
    context_object_name = 'course'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

     # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HodUpdateCourse, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context
    
# HOD Delete Course
class HodDeleteCourse(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Course
    template_name = 'info/hod/course_confirm_delete.html'
    success_url = reverse_lazy('info:department_courses')
    success_message = "Course was successfully deleted."
    context_object_name = 'course'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Classes in the Department
class DepartmentClasses(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/dept_classes.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def get_context_data(self, **kwargs):
        context = super(DepartmentClasses, self).get_context_data(**kwargs)
        context['class_list'] = Class.objects.filter(department_id=self.request.user.teacher.department_id)
        return context

# HOD Create Class
class HodCreateClass(LoginRequiredMixin, CreateView):
    model = Class
    fields = ['id', 'section', 'semester']
    template_name = 'info/hod/class_form.html'
    success_url = reverse_lazy('info:department_classes')

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        obj = request.POST
        Class.objects.create(
            id=obj['id'],
            section=obj['section'], 
            semester=obj['semester'], 
            department_id=self.request.user.teacher.department_id
        ).save()
        messages.success(request, "Course was successfully created.")
        return redirect(self.success_url)
    
# HOD Delete Class
class HodDeleteClass(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Class
    template_name = 'info/hod/class_confirm_delete.html'
    success_url = reverse_lazy('info:department_classes')
    success_message = "Class was successfully deleted."
    context_object_name = 'class'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# HOD views Class Details
class HodClassDetail(LoginRequiredMixin, DetailView):
    model = Class
    template_name = 'info/hod/class_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Teachers in the Department
class DepartmentTeachers(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/dept_teachers.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def get_context_data(self, **kwargs):
        context = super(DepartmentTeachers, self).get_context_data(**kwargs)
        context['teacher_list'] = Teacher.objects.filter(department_id=self.request.user.teacher.department_id)
        return context

# HOD Update Teacher
class HodUpdateTeacher(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Teacher
    fields = ['name', 'gender']
    template_name = 'info/hod/teacher_form.html'
    success_url = reverse_lazy('info:department_teachers')
    success_message = "Teacher was successfully updated."
    context_object_name = 'teacher'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HodUpdateTeacher, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context

# Students in the Department
class DepartmentStudents(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/dept_students.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
    def get_context_data(self, **kwargs):
        context = super(DepartmentStudents, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.filter(class_id__department_id=self.request.user.teacher.department_id)
        return context

# HOD Update Student
class HodUpdateStudent(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = ['name', 'gender', 'date_of_birth', 'class_id']
    template_name = 'info/hod/student_form.html'
    success_url = reverse_lazy('info:department_students')
    success_message = "Student was successfully updated."
    context_object_name = 'student'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HodUpdateStudent, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context
    
# HOD Assign Details
class HodAssignDetail(LoginRequiredMixin, DetailView):
    model = Assign
    template_name = 'info/hod/assign_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Department Timetable
class DepartmentTimetable(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/timetable.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            class_list = Class.objects.filter(department_id=self.request.user.teacher.department_id)
            class_matrix = [[['' for period in range(12)] for day in range(6)] for c in range(len(class_list))]
            class_names = []

            for c, class_id in zip(range(len(class_list)), class_list):
                name = "Sem '"+ str(class_id.semester) + "' Section '" + class_id.section + "'"
                class_names.append(name)
                assign_time = AssignTime.objects.filter(assign__class_id=class_id)
                for row, day in enumerate(days_of_week):
                    t = 0
                    for col in range(12):
                        if col == 0:
                            class_matrix[c][row][0] = day[0]
                            continue
                        if col == 4 or col == 8:
                            continue
                        try:
                            a = assign_time.get(period=time_slots[t][0], day=day[0])
                            # class_matrix[c][row][col] = a.assign.course_id + "-" + a.assign.teacher.name
                            class_matrix[c][row][col] = a.assign
                        except AssignTime.DoesNotExist:
                            pass
                        t += 1
            
            context['timetable'] = class_matrix
            context['class_names'] = class_names
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# HOD views Teacher Timetable
class TeacherTimetableView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/teacher_timetable.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            teacher_id = kwargs['teacher_id']
            assign_time = AssignTime.objects.filter(assign__teacher_id=teacher_id)
            class_matrix = [[True for period in range(12)] for day in range(6)]
            for row, day in enumerate(days_of_week):
                t = 0
                for col in range(12):
                    if col == 0:
                        class_matrix[row][0] = day[0]
                        continue
                    if col == 4 or col == 8:
                        continue
                    try:
                        a = assign_time.get(period=time_slots[t][0], day=day[0])
                        class_matrix[row][col] = a
                    except AssignTime.DoesNotExist:
                        pass
                    t += 1
            
            context['timetable'] = class_matrix
            context['teacher_name'] = Teacher.objects.get(teacher_id=teacher_id).name
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# HOD Assign Teacher to Class and Course
class HodCreateAssign(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Assign
    fields = ['teacher', 'class_id', 'course']
    template_name = 'info/hod/assign_form.html'
    success_url = reverse_lazy('info:manage_department')
    success_message = "Teacher was successfully assigned to Class and Course."
    context_object_name = 'assign'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# HOD Update Assign
class HodUpdateAssign(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Assign
    fields = ['teacher', 'class_id', 'course']
    template_name = 'info/hod/assign_form.html'
    success_url = reverse_lazy('info:manage_department')
    success_message = "Teacher was successfully updated."
    context_object_name = 'assign'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HodUpdateAssign, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context

# Delete Assign
class HodDeleteAssign(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Assign
    template_name = 'info/hod/assign_confirm_delete.html'
    success_url = reverse_lazy('info:manage_department')
    success_message = "Teacher was successfully unassigned from Class and Course."
    context_object_name = 'assign'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        # self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Assign Time Slots
class HodAssignTimeSlots(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssignTime
    fields = ['assign', 'period', 'day']
    template_name = 'info/hod/assign_time_form.html'
    success_url = reverse_lazy('info:manage_department')
    success_message = "Time slots were successfully assigned."
    context_object_name = 'assign_time'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Delete Time Slots
class HodDeleteTimeSlots(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = AssignTime
    template_name = 'info/hod/assign_time_confirm_delete.html'
    success_url = reverse_lazy('info:manage_department')
    success_message = "Time slots were successfully deleted."
    context_object_name = 'assign_time'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# HOD views Student Attendance
class HodStudentAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/student_attendance.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            roll_number = kwargs['roll_number']
            student = Student.objects.get(roll_number=roll_number)
            assign_list = Assign.objects.filter(class_id_id=student.class_id)
            attendance_list = []
            for assign in assign_list:
                try:
                    attendance = AttendanceTotal.objects.get(student=student, course=assign.course)
                except AttendanceTotal.DoesNotExist:
                    attendance = AttendanceTotal(student=student, course=assign.course)
                    attendance.save()
                attendance_list.append(attendance)
            context['attendance_list'] = attendance_list
            context['class_id'] = student.class_id.id
            context['student_name'] = student.name
            context['roll_number'] = roll_number
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# HOD Views Student Attendance Detail View
class HodStudentAttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/student_attendance_detail.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            roll_number = kwargs['roll_number']
            course_id = kwargs['course_id']
            student = get_object_or_404(Student, roll_number=roll_number)
            course = get_object_or_404(Course, id=course_id)
            attendance_list = Attendance.objects.filter(course=course, student=student).order_by('date')
            context['attendance_list'] = attendance_list
            context['course'] = course
            context['student'] = student
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Change Attendance
class HodChangeAttendance(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        attendance_id = kwargs['attendance_id']
        attendance = get_object_or_404(Attendance, id=attendance_id)
        attendance.status = not attendance.status
        attendance.save()
        return HttpResponseRedirect(reverse_lazy('info:hod_student_attendance_detail', kwargs={'roll_number': attendance.student.roll_number, 'course_id': attendance.course_id}))


# Hod views Student Marks
class HodStudentMarksListView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/student_marks_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            roll_number = kwargs['roll_number']
            student = Student.objects.get(roll_number=roll_number)
            assign_list = Assign.objects.filter(class_id_id=student.class_id)
            student_course_list = []
            for assign in assign_list:
                try:
                    student_course = StudentCourse.objects.get(student=student, course=assign.course)
                except:
                    student_course = StudentCourse(student=student, course=assign.course)
                    student_course.save()
                    student_course.marks_set.create(name = 'Midterm 1')
                    student_course.marks_set.create(name = 'Midterm 2')
                    student_course.marks_set.create(name = 'Midterm 3')
                    student_course.marks_set.create(name = 'Event 1')
                    student_course.marks_set.create(name = 'Event 2')
                    student_course.marks_set.create(name = 'Semester Final Exam')
                student_course_list.append(student_course)
            context['student_course_list'] = student_course_list
            context['class_id'] = student.class_id.id
            context['student_name'] = student.name
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# HOD View Courses for Teacher
class HodViewCoursesForTeacherView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/courses_for_teacher.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            teacher_id = kwargs['teacher_id']
            course_list = Assign.objects.filter(teacher=teacher_id)
            context['course_list'] = course_list
            context['teacher_name'] = Teacher.objects.get(teacher_id=teacher_id).name
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# HOD Reports View 
class HodReportClassesView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/class_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_hod:
            context = self.get_context_data(**kwargs)
            class_list = Class.objects.filter(department=self.request.user.teacher.department_id)
            context['class_list'] = class_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# HOD Generate Report
class HodReportView(LoginRequiredMixin, TemplateView):
    template_name = 'info/hod/class_report.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            class_id = kwargs['class_id']
            assign_list = Assign.objects.filter(class_id=class_id)
            student_course_list = []
            for assign in assign_list:
                for student in assign.class_id.student_set.all():
                    try:
                        student_course = StudentCourse.objects.get(student=student, course=assign.course)
                    except StudentCourse.DoesNotExist:
                        student_course = StudentCourse.objects.create(student=student, course=assign.course)
                        student_course.save()
                    obj = StudentCourse.objects.get(student=student, course=assign.course)
                    student_course_list.append(obj)
            context['class'] = Class.objects.get(id=class_id)
            context['student_count'] = Student.objects.filter(class_id=class_id).count()
            context['student_course_list'] = student_course_list
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# ================== Inline Formset Views for Admin ================== #

# Department Details
class DepartmentDetail(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'info/admin/department_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

# Edit Classes for Department
class DepartmentClassEditView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Department
    template_name = 'info/admin/department_class_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Department.objects.all())
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Department.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class = None):
        return DepartmentClassFormset(**self.get_form_kwargs(), instance=self.object)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Changes were saved for Classes.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('info:department_detail', kwargs={'pk': self.object.pk})
    
# Class Details
class ClassDetail(LoginRequiredMixin, DetailView):
    model = Class
    template_name = 'info/admin/class_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Edit Students for Class
class ClassStudentEditView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Class
    template_name = 'info/admin/class_student_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Class.objects.all())
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Class.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class = None):
        return ClassStudentFormset(**self.get_form_kwargs(), instance=self.object)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Changes were saved for Students.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('info:class_detail', kwargs={'pk': self.object.pk})
    
# Assign Details
class AssignDetail(LoginRequiredMixin, DetailView):
    model = Assign
    template_name = 'info/admin/assign_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Edit AssignTime for Assign
class AssignTimeEditView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Assign
    template_name = 'info/admin/assign_time_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Assign.objects.all())
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Assign.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class = None):
        return AssignTimeFormset(**self.get_form_kwargs(), instance=self.object)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Changes were saved for Teacher.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('info:assign_detail', kwargs={'pk': self.object.pk})
    
# Student Course Details
class StudentCourseDetail(LoginRequiredMixin, DetailView):
    model = StudentCourse
    template_name = 'info/admin/student_course_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)
    
# Edit Marks for Student Course
class StudentCourseMarksEditView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = StudentCourse
    template_name = 'info/admin/student_course_marks_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StudentCourse.objects.all())
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=StudentCourse.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class = None):
        return StudentCourseMarksFormset(**self.get_form_kwargs(), instance=self.object)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Changes were saved for Marks.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('info:student_course_detail', kwargs={'pk': self.object.pk})
    
# Marks Update View
class UpdateMarks(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Marks
    fields = ['name', 'marks1']
    template_name = 'info/admin/marks_form.html'
    success_message = "Marks was successfully updated."
    context_object_name = 'marks'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = None
        if not request.user.is_superuser:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

     # Add your context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(UpdateMarks, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form_type'] = 'Update'
        return context
    
    def get_success_url(self):
        return reverse('info:student_course_detail', kwargs={'pk': self.object.student_course.pk})
    
# ================== Inline Formset Views for HOD ================== #

# HOD Edits Periods for Teacher
class HodAssignTimeEditView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Assign
    template_name = 'info/hod/assign_time_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Assign.objects.all())
        if not request.user.is_hod:
            return redirect('info:unauthorize_view')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Assign.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class = None):
        return AssignTimeFormset(**self.get_form_kwargs(), instance=self.object)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Changes were saved for Teacher.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('info:hod_assign_detail', kwargs={'pk': self.object.pk})
