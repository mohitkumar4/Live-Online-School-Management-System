from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    progress_percentage = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    def update_progress(self):
        from lessons.models import Lesson, LessonProgress
        
        total_lessons = Lesson.objects.filter(course=self.course, is_published=True).count()
        if total_lessons == 0:
            self.progress_percentage = 0
        else:
            completed_lessons = LessonProgress.objects.filter(
                user=self.user,
                lesson__course=self.course,
                is_completed=True
            ).count()
            self.progress_percentage = int((completed_lessons / total_lessons) * 100)
        
        # Mark as completed if 100%
        if self.progress_percentage >= 100 and not self.is_completed:
            self.is_completed = True
            from django.utils import timezone
            self.completed_at = timezone.now()
        
        self.save()

