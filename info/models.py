from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False, verbose_name='Student Status')
    is_teacher = models.BooleanField(default=False, verbose_name='Teacher Status')