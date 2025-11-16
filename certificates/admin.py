from django.contrib import admin
from .models import Certificate, CertificateTemplate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'certificate_number', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('user__username', 'course__title', 'certificate_number')
    readonly_fields = ('certificate_number', 'issued_at')


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at')

