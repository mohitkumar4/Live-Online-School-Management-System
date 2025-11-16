from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course
from .models import Enrollment


@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, status='published')
    
    # Check if already enrolled
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('courses:course_detail', slug=slug)
    
    # Create enrollment
    enrollment = Enrollment.objects.create(user=request.user, course=course)
    messages.success(request, f'Successfully enrolled in {course.title}!')
    
    # Update course enrollment count
    course.total_enrollments = Enrollment.objects.filter(course=course).count()
    course.save()
    
    # Redirect to first lesson if available, otherwise to course detail
    first_lesson = course.lessons.filter(is_published=True).order_by('order').first()
    if first_lesson:
        return redirect('lessons:lesson_detail', course_slug=course.slug, lesson_slug=first_lesson.slug)
    else:
        return redirect('courses:course_detail', slug=course.slug)


@login_required
def unenroll(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    
    if enrollment:
        enrollment.delete()
        messages.success(request, f'Unenrolled from {course.title}.')
        
        # Update course enrollment count
        course.total_enrollments = Enrollment.objects.filter(course=course).count()
        course.save()
    else:
        messages.error(request, 'You are not enrolled in this course.')
    
    return redirect('dashboard:my_courses')

