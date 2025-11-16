from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from enrollments.models import Enrollment
from .models import Certificate, CertificateTemplate
from courses.models import Course


@login_required
def generate_certificate(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    # Check if course is completed
    if not enrollment.is_completed or enrollment.progress_percentage < 100:
        messages.error(request, 'You must complete the course to generate a certificate.')
        return redirect('courses:course_detail', slug=course_slug)
    
    # Check if certificate already exists
    certificate, created = Certificate.objects.get_or_create(
        enrollment=enrollment,
        defaults={
            'course': course,
            'user': request.user,
        }
    )
    
    if created:
        messages.success(request, 'Certificate generated successfully!')
    else:
        messages.info(request, 'Certificate already exists.')
    
    return redirect('certificates:certificate_detail', certificate_number=certificate.certificate_number)


@login_required
def certificate_detail(request, certificate_number):
    certificate = get_object_or_404(Certificate, certificate_number=certificate_number)
    
    # Only allow the certificate owner to view it
    if certificate.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this certificate.')
        return redirect('dashboard:index')
    
    template = CertificateTemplate.objects.filter(is_default=True).first()
    if not template:
        template = CertificateTemplate.objects.first()
    
    context = {
        'certificate': certificate,
        'template': template,
    }
    return render(request, 'certificates/certificate_detail.html', context)


@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user).order_by('-issued_at')
    
    context = {
        'certificates': certificates,
    }
    return render(request, 'certificates/my_certificates.html', context)

