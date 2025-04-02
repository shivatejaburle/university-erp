from django import forms
from django.forms import ModelForm
from info.models import User, Department, Course, Class, Teacher, Student

class AdminForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(AdminForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match...!"
            )
        
class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['id', 'name']
        labels = {
            'id': 'Department ID',
            'name': 'Department Name',
        }

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['department', 'id', 'name', 'short_name']

class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['department', 'id', 'section', 'semester']

class TeacherForm(ModelForm):
    email_address = forms.EmailField()
    class Meta:
        model = Teacher
        fields = ['name', 'gender', 'date_of_birth', 'teacher_id', 'department']
        labels = {
            'name': 'Teacher Full Name',
            'teacher_id': 'Teacher ID',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class StudentForm(ModelForm):
    email_address = forms.EmailField()
    class Meta:
        model = Student
        fields = ['name', 'gender', 'date_of_birth', 'roll_number', 'class_id']
        labels = {
            'name': 'Student Full Name',
            'class_id': 'Class',
            'date_of_birth': 'Date of Birth',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

