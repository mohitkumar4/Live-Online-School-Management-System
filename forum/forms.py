from django import forms
from .models import Discussion, DiscussionReply


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter discussion title'}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control', 'placeholder': 'Enter your question or discussion topic...'}),
        }


class DiscussionReplyForm(forms.ModelForm):
    class Meta:
        model = DiscussionReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Write your reply...'}),
        }

