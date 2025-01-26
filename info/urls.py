from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index_view'),
]