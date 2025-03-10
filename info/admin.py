from django.contrib import admin
from info.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_student', 'is_teacher')

admin.site.register(User, UserAdmin)