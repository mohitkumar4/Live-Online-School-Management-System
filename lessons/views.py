from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course
from enrollments.models import Enrollment
from .models import Lesson, LessonProgress
from django.db.models import Q


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, status='published')
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, is_published=True)
    
    # Check enrollment or if lesson is preview
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    is_enrolled = enrollment is not None
    
    if not lesson.is_preview and not is_enrolled:
        messages.error(request, 'You must enroll in this course to access this lesson.')
        return redirect('courses:course_detail', slug=course_slug)
    
    # Get all lessons for navigation
    all_lessons = Lesson.objects.filter(course=course, is_published=True).order_by('order')
    
    # Get previous and next lessons
    prev_lesson = None
    next_lesson = None
    lesson_index = None
    
    for index, l in enumerate(all_lessons):
        if l.id == lesson.id:
            lesson_index = index
            if index > 0:
                prev_lesson = all_lessons[index - 1]
            if index < len(all_lessons) - 1:
                next_lesson = all_lessons[index + 1]
            break
    
    # Get or create progress
    progress = None
    if is_enrolled:
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
    
    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'lesson_index': lesson_index,
        'progress': progress,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'lessons/lesson_detail.html', context)


@login_required
def mark_complete(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    
    # Check enrollment
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        messages.error(request, 'You must be enrolled in this course.')
        return redirect('courses:course_detail', slug=course_slug)
    
    # Mark as complete
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    progress.is_completed = True
    progress.save()
    
    # Update enrollment progress
    enrollment.update_progress()
    
    messages.success(request, 'Lesson marked as complete!')
    return redirect('lessons:lesson_detail', course_slug=course_slug, lesson_slug=lesson_slug)

