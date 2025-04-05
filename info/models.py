from django.db import models
from django.contrib.auth.models import AbstractUser
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from django.db.models.signals import post_save, post_delete
from django.urls import reverse

# ================== Constants ================== #
gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

time_slots = (
    ('07:30 AM - 08:30 AM', '07:30 AM - 08:30 AM'),
    ('08:30 AM - 09:30 AM', '08:30 AM - 09:30 AM'),
    ('09:30 AM - 10:30 AM', '09:30 AM - 10:30 AM'),
    ('11:00 AM - 11:50 PM', '11:00 AM - 11:50 PM'),
    ('11:50 AM - 12:40 PM', '11:50 AM - 12:40 PM'),
    ('12:40 PM - 01:30 PM', '12:40 PM - 01:30 PM'),
    ('02:30 PM - 03:30 PM', '02:30 PM - 03:30 PM'),
    ('03:30 PM - 04:30 PM', '03:30 PM - 04:30 PM'),
    ('04:30 PM - 05:30 PM', '04:30 PM - 05:30 PM'),
)

days_of_week = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

exam_name = (
    ('Midterm 1', 'Midterm 1'),
    ('Midterm 2', 'Midterm 2'),
    ('Midterm 3', 'Midterm 3'),
    ('Event 1', 'Event 1'),
    ('Event 2', 'Event 2'),
    ('Semester Final Exam', 'Semester Final Exam'),
)

# ================== Models ================== #

class User(AbstractUser):
    is_student = models.BooleanField(default=False, verbose_name='Student Status')
    is_teacher = models.BooleanField(default=False, verbose_name='Teacher Status')

# Department
class Department(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('info:department_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
    
# Course
class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, default='X')

    def __str__(self): 
        return self.name
    
# Class
class Class(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    id = models.CharField(max_length=50, primary_key=True)
    section = models.CharField(max_length=50)
    semester = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Classes'

    def get_absolute_url(self):
        return reverse('info:class_detail', kwargs={'pk': self.pk})

    def __str__(self):
        dept = Department.objects.get(name = self.department)
        return dept.name + ' : ' + str(self.semester) + ' ' + self.section
    
# Student
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default='1')
    roll_number = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, choices=gender_choices, default='Male')
    date_of_birth = models.DateField(default='1990-21-10')

    def __str__(self):
        return self.name

# Teacher
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    teacher_id = models.CharField(max_length=50, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default='1')
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, choices=gender_choices, default='Male')
    date_of_birth = models.DateField(default='1970-21-10')

    def __str__(self):
        return self.name
    
# Assign Class and Course to Teacher
class Assign(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'class_id', 'teacher')

    def get_absolute_url(self):
        return reverse('info:assign_detail', kwargs={'pk': self.pk})

    def __str__(self):
        cl = Class.objects.get(id = self.class_id_id)
        course = Course.objects.get(id = self.course_id)
        teacher = Teacher.objects.get(teacher_id = self.teacher_id)
        return str(teacher.name) + ' : ' +  str(course.short_name) + ' : ' + str(cl)
    
# Assign Time Slots
class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=time_slots, default='07:30 AM - 08:30 AM')
    day = models.CharField(max_length=50, choices=days_of_week)

# Attendance Class
class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'

# Attendance Student
class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendanceClass = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE, default='1')
    date = models.DateField(default='2025-03-22')
    status = models.BooleanField(default=True)

    def __str__(self):
        student_name = Student.objects.get(name = self.student)
        course_name = Course.objects.get(name = self.course)
        return student_name.name + ' : ' + course_name.name

# Total Attendance
class AttendanceTotal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course')

    @property
    def attendance_class(self):
        student = Student.objects.get(name = self.student)
        course = Course.objects.get(name = self.course)
        attendance_class = Attendance.objects.filter(student = student, course = course, status = 'True').count()
        return attendance_class
    
    @property
    def total_class(self):
        student = Student.objects.get(name = self.student)
        course = Course.objects.get(name = self.course)
        total_class = Attendance.objects.filter(student = student, course = course).count()
        return total_class
    
    @property
    def attendance(self):
        student = Student.objects.get(name = self.student)
        course = Course.objects.get(name = self.course)
        total_class = Attendance.objects.filter(student = student, course = course).count()
        attendance_class = Attendance.objects.filter(student = student, course = course, status = 'True').count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round((attendance_class / total_class) * 100, 2)
        return attendance
    
    @property
    def classes_to_attend(self):
        student = Student.objects.get(name = self.student)
        course = Course.objects.get(name = self.course)
        total_class = Attendance.objects.filter(student = student, course = course).count()
        attendance_class = Attendance.objects.filter(student = student, course = course, status = 'True').count()
        classes_to_attend = math.ceil((0.75 * total_class - attendance_class) / 0.25)
        if classes_to_attend < 0:
            return 0
        return classes_to_attend
    
# Student Course
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course')
        verbose_name_plural = 'Marks'

    def get_absolute_url(self):
        return reverse('info:student_course_detail', kwargs={'pk': self.pk})

    def __str__(self):
        student = Student.objects.get(name = self.student)
        course = Course.objects.get(name = self.course)
        return student.name + ' : ' + course.name
    
    # CIE - Continuous Internal Evaluation
    def get_cie(self):
        marks_list = self.marks_set.all()
        marks = []
        for m in marks_list:
            marks.append(m.marks1)
        cie = math.ceil(sum(marks[:5]) / 2)
        return cie
    
    def get_attendance(self):
        a_obj = AttendanceTotal.objects.get(student = self.student, course = self.course)
        return a_obj.attendance

# Marks
class Marks(models.Model):
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=exam_name, default='Midterm 1')
    marks1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        unique_together = ('student_course', 'name')

    @property
    def total_marks(self):
        if self.name == 'Semester Final Exam':
            return 100
        else:
            return 20
        
# Marks Class
class MarksClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=exam_name, default='Midterm 1')
    status = models.BooleanField(default='False')

    class Meta:
        unique_together = ('assign', 'name')

    @property
    def total_marks(self):
        if self.name == 'Semester Final Exam':
            return 100
        else:
            return 20

# Attendance Range
class AttendanceRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

# ================== Triggers ================== #

# Date Range
def dateRange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Create Attendance when new Student is Created
days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}
def create_attendance(sender, instance, **kwargs):
    if kwargs['created']:
        start_date = AttendanceRange.objects.all().first().start_date
        end_date = AttendanceRange.objects.all().first().end_date
        for date in dateRange(start_date, end_date):
            if date.isoweekday() == days[instance.day]:
                try:
                    AttendanceClass.objects.get(assign = instance.assign, date = date.strftime('%Y-%m-%d'))
                except AttendanceClass.DoesNotExist:
                    a_obj= AttendanceClass.objects.create(assign = instance.assign, date = date.strftime('%Y-%m-%d'))
                    a_obj.save()

# Create Marks when new Student or Course is Created
def create_marks(sender, instance, **kwargs):
    if kwargs['created']:
        if hasattr(instance, 'name'):
            assign_list = instance.class_id.assign_set.all()
            for assign in assign_list:
                try:
                    StudentCourse.objects.get(student = instance, course = assign.course)
                except StudentCourse.DoesNotExist:
                    student_course = StudentCourse.objects.create(student = instance, course = assign.course)
                    student_course.save()
                    student_course.marks_set.create(name = 'Midterm 1')
                    student_course.marks_set.create(name = 'Midterm 2')
                    student_course.marks_set.create(name = 'Midterm 3')
                    student_course.marks_set.create(name = 'Event 1')
                    student_course.marks_set.create(name = 'Event 2')
                    student_course.marks_set.create(name = 'Semester Final Exam')
                    student_course.save()
        elif hasattr(instance, 'course'):
            student_list = instance.class_id.student_set.all()
            course = instance.course
            for student in student_list:
                try:
                    StudentCourse.objects.get(student = student, course = course)
                except StudentCourse.DoesNotExist:
                    student_course = StudentCourse.objects.create(student = student, course = course)
                    student_course.save()
                    student_course.marks_set.create(name = 'Midterm 1')
                    student_course.marks_set.create(name = 'Midterm 2')
                    student_course.marks_set.create(name = 'Midterm 3')
                    student_course.marks_set.create(name = 'Event 1')
                    student_course.marks_set.create(name = 'Event 2')
                    student_course.marks_set.create(name = 'Semester Final Exam')
                    student_course.save()

# Create Marks Class
def create_marks_class(sender, instance, **kwargs):
    if kwargs['created']:
        for name in exam_name:
            try:
                MarksClass.objects.get(assign = instance, name = name[0])
            except MarksClass.DoesNotExist:
                m_obj = MarksClass.objects.create(assign = instance, name = name[0])
                m_obj.save()

# Delete Marks
def delete_marks(sender, instance, **kwargs):
    student_list = instance.class_id.student_set.all()
    StudentCourse.objects.filter(course = instance.course, student__in = student_list).delete()

# ================== Signals ================== #
post_save.connect(create_marks, sender=Student)
post_save.connect(create_marks, sender=Assign)
post_save.connect(create_marks_class, sender=Assign)
post_save.connect(create_attendance, sender=AssignTime)
post_delete.connect(delete_marks, sender=Assign)