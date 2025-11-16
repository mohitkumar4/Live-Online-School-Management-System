from django import forms
from .models import Course, CourseReview


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'short_description', 'category', 'thumbnail',
            'difficulty_level', 'language', 'duration_hours', 'learning_outcomes',
            'requirements', 'status', 'is_free', 'price', 'tags'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'learning_outcomes': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., python, web development, django'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

