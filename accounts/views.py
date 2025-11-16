from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Avg
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from .models import User, UserProfile
from enrollments.models import Enrollment
from courses.models import Course, CourseReview
from lessons.models import LessonProgress
from certificates.models import Certificate
from quizzes.models import QuizAttempt


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('dashboard:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    profile_obj, created = UserProfile.objects.get_or_create(user=user)
    
    # Get statistics based on user role
    stats = {}
    
    if user.is_student:
        # Student Statistics
        stats['total_enrollments'] = Enrollment.objects.filter(user=user).count()
        stats['completed_courses'] = Enrollment.objects.filter(user=user, is_completed=True).count()
        stats['certificates'] = Certificate.objects.filter(user=user).count()
        stats['total_lessons_completed'] = LessonProgress.objects.filter(user=user, is_completed=True).count()
        stats['total_quizzes_taken'] = QuizAttempt.objects.filter(user=user).count()
        stats['quizzes_passed'] = QuizAttempt.objects.filter(user=user, passed=True).count()
        stats['recent_enrollments'] = Enrollment.objects.filter(user=user).order_by('-enrolled_at')[:5]
        
    elif user.is_instructor:
        # Instructor Statistics
        stats['total_courses'] = Course.objects.filter(instructor=user).count()
        stats['published_courses'] = Course.objects.filter(instructor=user, status='published').count()
        stats['total_enrollments'] = Enrollment.objects.filter(course__instructor=user).count()
        stats['total_students'] = Enrollment.objects.filter(course__instructor=user).values('user').distinct().count()
        avg_rating = CourseReview.objects.filter(course__instructor=user).aggregate(Avg('rating'))['rating__avg'] or 0
        stats['avg_rating'] = round(avg_rating, 2)
        stats['total_reviews'] = CourseReview.objects.filter(course__instructor=user).count()
        stats['recent_courses'] = Course.objects.filter(instructor=user).order_by('-created_at')[:5]
        
    else:
        # Admin Statistics
        stats['total_courses'] = Course.objects.count()
        stats['published_courses'] = Course.objects.filter(status='published').count()
        stats['total_users'] = User.objects.count()
        stats['total_instructors'] = User.objects.filter(role='instructor').count()
        stats['total_students'] = User.objects.filter(role='student').count()
        stats['total_enrollments'] = Enrollment.objects.count()
        stats['total_certificates'] = Certificate.objects.count()
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        p_form = ProfileUpdateForm(request.POST, instance=profile_obj)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile_obj)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'profile': profile_obj,
        'stats': stats,
    }
    return render(request, 'accounts/profile.html', context)


def instructor_profile(request, username):
    instructor = User.objects.get(username=username, role='instructor')
    context = {
        'instructor': instructor,
    }
    return render(request, 'accounts/instructor_profile.html', context)

