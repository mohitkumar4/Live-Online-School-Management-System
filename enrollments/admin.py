from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'is_completed', 'progress_percentage', 'completed_at')
    list_filter = ('is_completed', 'enrolled_at', 'completed_at')
    search_fields = ('user__username', 'course__title')
    readonly_fields = ('enrolled_at', 'completed_at', 'progress_percentage')

