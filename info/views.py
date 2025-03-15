from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Index View
class IndexView(TemplateView):
    template_name = 'info/index.html'

# Admin View
class AdminView(LoginRequiredMixin, TemplateView):
    template_name = 'info/admin/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# Teacher View
class TeacherView(LoginRequiredMixin, TemplateView):
    template_name = 'info/teacher/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')

# Student View
class StudentView(LoginRequiredMixin, TemplateView):
    template_name = 'info/student/index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        return redirect('info:unauthorize_view')
    
# Authorize View
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