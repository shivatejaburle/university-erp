from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('login_success/', views.login_success, name = 'login_success'),
    path('unauthorized_access/', views.UnauthorizeView.as_view(), name='unauthorize_view'),
    path('', views.IndexView.as_view(), name = 'index_view'),
    path('admin_home/', views.AdminView.as_view(), name = 'admin_view'),
    path('teacher/', views.TeacherView.as_view(), name = 'teacher_view'),
    path('student/', views.StudentView.as_view(), name = 'student_view'),
]