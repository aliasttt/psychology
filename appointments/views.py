from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import AppointmentForm
from .models import Appointment


def appointment_request(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            
            # Send email notification to admin
            try:
                subject = f'New Appointment Request from {appointment.full_name}'
                message = render_to_string('appointments/email_notification.txt', {
                    'appointment': appointment
                })
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],  # Send to admin email
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't fail the request
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Your appointment request has been submitted successfully! We will contact you soon.')
            return redirect('appointments:success')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/appointment_form.html', {'form': form})


def appointment_success(request):
    return render(request, 'appointments/success.html')
