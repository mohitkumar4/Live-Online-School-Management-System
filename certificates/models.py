from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Course
from enrollments.models import Enrollment
import uuid

User = get_user_model()


class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    certificate_number = models.CharField(max_length=100, unique=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='certificates/pdf/', blank=True, null=True)
    
    class Meta:
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.certificate_number}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = f"CERT-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('certificates:certificate_detail', kwargs={'certificate_number': self.certificate_number})


class CertificateTemplate(models.Model):
    name = models.CharField(max_length=100)
    template_html = models.TextField(help_text="HTML template for certificate")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_default:
            CertificateTemplate.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

