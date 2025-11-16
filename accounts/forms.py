from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture', 
                 'bio', 'phone_number', 'date_of_birth', 'address', 'city', 'country']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['occupation', 'education_level', 'interests', 'website', 
                 'linkedin_profile', 'twitter_profile', 'github_profile']
        widgets = {
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'twitter_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourhandle'}),
            'github_profile': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/yourusername'}),
        }

