from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification
            try:
                subject = f'New Contact Form Submission: {contact_message.subject}'
                message = f"""
New contact form submission:

Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone or 'Not provided'}

Subject: {contact_message.subject}

Message:
{contact_message.message}

---
This message was sent from the contact form on {request.get_host()}
                """
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact:success')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/success.html')
