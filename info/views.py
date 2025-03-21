from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from info.models import User
from django.contrib import messages
from info.forms import AdminForm
from allauth.account.models import EmailAddress

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

# Create Admin User
class CreateAdminUser(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    # fields = ['username', 'email', 'is_superuser']
    form_class = AdminForm
    template_name = 'info/admin/create_admin_user.html'
    success_url = '/admin_home/'
    
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