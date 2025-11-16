from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from courses.models import Course, CourseReview
from enrollments.models import Enrollment
from lessons.models import LessonProgress
from certificates.models import Certificate
from quizzes.models import QuizAttempt

User = get_user_model()


@login_required
def index(request):
    user = request.user
    
    if user.is_student:
        # Student Dashboard
        enrollments = Enrollment.objects.filter(user=user).order_by('-enrolled_at')[:5]
        total_enrollments = Enrollment.objects.filter(user=user).count()
        completed_courses = Enrollment.objects.filter(user=user, is_completed=True).count()
        certificates = Certificate.objects.filter(user=user).count()
        
        # Recent progress
        recent_progress = LessonProgress.objects.filter(user=user).order_by('-updated_at')[:5]
        
        # Statistics
        total_lessons_completed = LessonProgress.objects.filter(user=user, is_completed=True).count()
        total_quizzes_taken = QuizAttempt.objects.filter(user=user).count()
        quizzes_passed = QuizAttempt.objects.filter(user=user, passed=True).count()
        
        context = {
            'enrollments': enrollments,
            'total_enrollments': total_enrollments,
            'completed_courses': completed_courses,
            'certificates': certificates,
            'recent_progress': recent_progress,
            'total_lessons_completed': total_lessons_completed,
            'total_quizzes_taken': total_quizzes_taken,
            'quizzes_passed': quizzes_passed,
        }
        template = 'dashboard/student_dashboard.html'
        
    elif user.is_instructor:
        # Instructor Dashboard
        courses = Course.objects.filter(instructor=user).order_by('-created_at')[:5]
        total_courses = Course.objects.filter(instructor=user).count()
        published_courses = Course.objects.filter(instructor=user, status='published').count()
        
        # Statistics
        total_enrollments = Enrollment.objects.filter(course__instructor=user).count()
        total_students = Enrollment.objects.filter(course__instructor=user).values('user').distinct().count()
        
        # Course ratings
        avg_rating = CourseReview.objects.filter(
            course__instructor=user
        ).aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Recent enrollments
        recent_enrollments = Enrollment.objects.filter(
            course__instructor=user
        ).order_by('-enrolled_at')[:5]
        
        context = {
            'courses': courses,
            'total_courses': total_courses,
            'published_courses': published_courses,
            'total_enrollments': total_enrollments,
            'total_students': total_students,
            'avg_rating': round(avg_rating, 2),
            'recent_enrollments': recent_enrollments,
        }
        template = 'dashboard/instructor_dashboard.html'
        
    else:
        # Admin Dashboard
        total_courses = Course.objects.count()
        published_courses = Course.objects.filter(status='published').count()
        total_users = User.objects.count()
        total_enrollments = Enrollment.objects.count()
        total_certificates = Certificate.objects.count()
        
        context = {
            'total_courses': total_courses,
            'published_courses': published_courses,
            'total_users': total_users,
            'total_enrollments': total_enrollments,
            'total_certificates': total_certificates,
        }
        template = 'dashboard/admin_dashboard.html'
    
    return render(request, template, context)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-enrolled_at')
    
    # Update progress for all enrollments
    for enrollment in enrollments:
        enrollment.update_progress()
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'dashboard/my_courses.html', context)


@login_required
def instructor_courses(request):
    if not request.user.is_instructor:
        messages.error(request, 'Only instructors can access this page.')
        return redirect('dashboard:index')
    
    courses = Course.objects.filter(instructor=request.user).order_by('-created_at')
    
    context = {
        'courses': courses,
    }
    return render(request, 'dashboard/instructor_courses.html', context)

