from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_request, name='appointment_request'),
    path('success/', views.appointment_success, name='success'),
]
