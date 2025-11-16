from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from courses.models import Course
from enrollments.models import Enrollment
from .models import Discussion, DiscussionReply
from .forms import DiscussionForm, DiscussionReplyForm


@login_required
def discussion_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, status='published')
    
    # Check enrollment
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    
    discussions = Discussion.objects.filter(course=course).order_by('-is_pinned', '-created_at')
    
    paginator = Paginator(discussions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'course': course,
        'discussions': page_obj,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'forum/discussion_list.html', context)


@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    
    # Check enrollment
    is_enrolled = Enrollment.objects.filter(user=request.user, course=discussion.course).exists()
    if not is_enrolled:
        messages.error(request, 'You must enroll in this course to view discussions.')
        return redirect('courses:course_detail', slug=discussion.course.slug)
    
    # Increment views
    discussion.views += 1
    discussion.save()
    
    replies = DiscussionReply.objects.filter(discussion=discussion).order_by('-is_answer', 'created_at')
    
    if request.method == 'POST':
        form = DiscussionReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.discussion = discussion
            reply.user = request.user
            reply.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('forum:discussion_detail', discussion_id=discussion.id)
    else:
        form = DiscussionReplyForm()
    
    context = {
        'discussion': discussion,
        'replies': replies,
        'form': form,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'forum/discussion_detail.html', context)


@login_required
def create_discussion(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, status='published')
    
    # Check enrollment
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    if not is_enrolled:
        messages.error(request, 'You must enroll in this course to create discussions.')
        return redirect('courses:course_detail', slug=course_slug)
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.course = course
            discussion.user = request.user
            discussion.save()
            messages.success(request, 'Discussion created successfully!')
            return redirect('forum:discussion_detail', discussion_id=discussion.id)
    else:
        form = DiscussionForm()
    
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'forum/create_discussion.html', context)


@login_required
def mark_as_answer(request, reply_id):
    reply = get_object_or_404(DiscussionReply, id=reply_id)
    discussion = reply.discussion
    
    # Only course instructor or discussion creator can mark as answer
    if discussion.course.instructor != request.user and discussion.user != request.user:
        messages.error(request, 'You do not have permission to mark this as answer.')
        return redirect('forum:discussion_detail', discussion_id=discussion.id)
    
    # Toggle answer status
    reply.is_answer = not reply.is_answer
    reply.save()
    
    messages.success(request, 'Answer status updated!')
    return redirect('forum:discussion_detail', discussion_id=discussion.id)

