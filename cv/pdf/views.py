from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
from django.shortcuts import render
from .forms import ContactForm
from django.shortcuts import get_object_or_404, redirect
from .forms import ContactForm
from .forms import CVForm
from .models import CV
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ContactForm()
    return render(request, 'pdf/contact.html', {'form': form})

def success_view(request):
    return render(request, "pdf/success.html")


def create_cv(request):
    if request.method == "POST":
        form = CVForm(request.POST, request.FILES) # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('cv_list') # Redirect to CV listing page
    else:
        form = CVForm()
        return render(request, 'pdf/cv_form.html', {'form': form})


def cv_list(request):
    CVs = CV.objects.all()
    return render(request, "pdf/cv_list.html",{"cvs": CVs})


def share_cv_email(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    recipient_email = request.POST.get('email')
    if recipient_email:
        subject = f"{cv.name}'s CV"
        message = f"Check out {cv.name}'s CV at {request.build_absolute_uri(cv.profile_picture.url)}"
        sender_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, sender_email, [recipient_email])
        messages.success(request, "CV shared successfully via email.")
    else:
        messages.error(request, "Please provide a valid email.")
    return redirect('cv_list')
