from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Course

User = get_user_model()


class Discussion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
    def get_absolute_url(self):
        return reverse('forum:discussion_detail', kwargs={'discussion_id': self.id})


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_replies')
    content = models.TextField()
    is_answer = models.BooleanField(default=False, help_text="Mark as correct answer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_answer', 'created_at']
        verbose_name_plural = "Discussion Replies"
    
    def __str__(self):
        return f"Reply to {self.discussion.title} by {self.user.username}"


class Comment(models.Model):
    """Generic comments for lessons"""
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment on {self.lesson.title} by {self.user.username}"

