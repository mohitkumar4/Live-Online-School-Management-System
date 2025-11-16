from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from lessons.models import Lesson

User = get_user_model()


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    time_limit_minutes = models.PositiveIntegerField(default=0, help_text="0 means no time limit")
    passing_score = models.PositiveIntegerField(default=70, help_text="Percentage required to pass")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='multiple_choice')
    order = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=1)
    explanation = models.TextField(blank=True, help_text="Explanation shown after answering")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.quiz.title} - {self.question_text[:50]}..."


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.choice_text[:30]}..."


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    percentage = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    time_taken_minutes = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.percentage}%"


class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    short_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.question_text[:30]}..."

