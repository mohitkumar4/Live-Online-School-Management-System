from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from courses.models import Course


class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='video')
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    
    # Video lesson fields
    video_url = models.URLField(blank=True, null=True, help_text="YouTube/Vimeo URL or direct video link")
    video_file = models.FileField(
        upload_to='lesson_videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv'])]
    )
    
    # Text lesson fields
    content = models.TextField(blank=True, null=True)
    
    # Resources
    resources = models.FileField(upload_to='lesson_resources/', blank=True, null=True)
    resources_url = models.URLField(blank=True, null=True)
    
    is_preview = models.BooleanField(default=False, help_text="Available for preview (non-enrolled users)")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('lessons:lesson_detail', kwargs={'course_slug': self.course.slug, 'lesson_slug': self.slug})


class LessonProgress(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    watched_duration = models.PositiveIntegerField(default=0, help_text="Watched duration in seconds")
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

