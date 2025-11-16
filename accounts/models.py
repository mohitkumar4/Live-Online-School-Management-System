from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User Model"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_instructor(self):
        return self.role == 'instructor' or self.is_staff
    
    @property
    def is_student(self):
        return self.role == 'student'


class UserProfile(models.Model):
    """Extended User Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    occupation = models.CharField(max_length=200, blank=True, null=True)
    education_level = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    twitter_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"

