from django.contrib import admin
from .models import Lesson, LessonProgress


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lesson_type', 'order', 'duration_minutes', 'is_published', 'created_at')
    list_filter = ('lesson_type', 'is_published', 'is_preview', 'created_at')
    search_fields = ('title', 'course__title', 'description')
    list_editable = ('order', 'is_published')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'watched_duration', 'completed_at')
    list_filter = ('is_completed', 'completed_at')
    search_fields = ('user__username', 'lesson__title')

