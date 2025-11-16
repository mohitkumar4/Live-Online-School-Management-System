from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from .models import Course, Category, CourseReview
from enrollments.models import Enrollment
from .forms import CourseForm, CourseReviewForm


def course_list(request):
    courses = Course.objects.filter(status='published')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    # Filter by free/paid
    is_free = request.GET.get('free', '')
    if is_free == 'true':
        courses = courses.filter(is_free=True)
    elif is_free == 'false':
        courses = courses.filter(is_free=False)
    
    # Ordering
    order_by = request.GET.get('order_by', '-created_at')
    if order_by in ['-created_at', '-rating', '-total_enrollments', 'title']:
        courses = courses.order_by(order_by)
    
    # Pagination
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.annotate(course_count=Count('courses')).order_by('-course_count')[:10]
    
    context = {
        'courses': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'selected_free': is_free,
        'order_by': order_by,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, status='published')
    
    # Check if user is enrolled
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None
    
    # Get reviews
    reviews = CourseReview.objects.filter(course=course).order_by('-created_at')[:10]
    review_count = CourseReview.objects.filter(course=course).count()
    
    # Check if user has reviewed
    user_review = None
    if request.user.is_authenticated:
        user_review = CourseReview.objects.filter(course=course, user=request.user).first()
    
    # Get related courses
    related_courses = Course.objects.filter(
        category=course.category,
        status='published'
    ).exclude(id=course.id)[:4]
    
    # Get first lesson for "Continue Learning" button
    from lessons.models import Lesson
    first_lesson = Lesson.objects.filter(course=course, is_published=True).order_by('order').first()
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'reviews': reviews,
        'review_count': review_count,
        'user_review': user_review,
        'related_courses': related_courses,
        'first_lesson': first_lesson,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def course_create(request):
    if not request.user.is_instructor:
        messages.error(request, 'Only instructors can create courses.')
        return redirect('courses:course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses:course_detail', slug=course.slug)
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_create.html', {'form': form})


@login_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    if course.instructor != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:course_detail', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_edit.html', {'form': form, 'course': course})


@login_required
def add_review(request, slug):
    course = get_object_or_404(Course, slug=slug, status='published')
    
    # Check if user is enrolled
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, 'You must enroll in the course before reviewing.')
        return redirect('courses:course_detail', slug=course.slug)
    
    # Check if user already reviewed
    review, created = CourseReview.objects.get_or_create(
        course=course,
        user=request.user,
        defaults={'rating': 1, 'comment': ''}
    )
    
    if request.method == 'POST':
        form = CourseReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            
            # Update course rating
            avg_rating = CourseReview.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg']
            course.rating = round(avg_rating, 2) if avg_rating else 0
            course.total_ratings = CourseReview.objects.filter(course=course).count()
            course.save()
            
            messages.success(request, 'Review added successfully!')
            return redirect('courses:course_detail', slug=course.slug)
    else:
        form = CourseReviewForm(instance=review)
    
    return render(request, 'courses/add_review.html', {'form': form, 'course': course})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(category=category, status='published')
    
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'courses': page_obj,
    }
    return render(request, 'courses/category_detail.html', context)

