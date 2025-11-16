from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from courses.models import Course
from enrollments.models import Enrollment
from .models import Quiz, Question, Choice, QuizAttempt, QuizAnswer


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Check enrollment
    enrollment = Enrollment.objects.filter(user=request.user, course=quiz.course).first()
    if not enrollment:
        messages.error(request, 'You must enroll in this course to take the quiz.')
        return redirect('courses:course_detail', slug=quiz.course.slug)
    
    # Get user's previous attempts
    previous_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-started_at')[:5]
    
    context = {
        'quiz': quiz,
        'previous_attempts': previous_attempts,
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Check enrollment
    enrollment = Enrollment.objects.filter(user=request.user, course=quiz.course).first()
    if not enrollment:
        messages.error(request, 'You must enroll in this course to take the quiz.')
        return redirect('courses:course_detail', slug=quiz.course.slug)
    
    # Create new attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        started_at=timezone.now()
    )
    
    return redirect('quizzes:take_quiz', attempt_id=attempt.id)


@login_required
def take_quiz(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    if attempt.completed_at:
        messages.info(request, 'You have already completed this quiz.')
        return redirect('quizzes:quiz_result', attempt_id=attempt.id)
    
    questions = Question.objects.filter(quiz=attempt.quiz).order_by('order')
    
    if request.method == 'POST':
        total_points = 0
        earned_points = 0
        
        for question in questions:
            total_points += question.points
            answer = QuizAnswer.objects.create(
                attempt=attempt,
                question=question,
            )
            
            if question.question_type == 'multiple_choice':
                choice_id = request.POST.get(f'question_{question.id}')
                if choice_id:
                    selected_choice = Choice.objects.filter(id=choice_id, question=question).first()
                    if selected_choice:
                        answer.selected_choice = selected_choice
                        answer.is_correct = selected_choice.is_correct
                        if selected_choice.is_correct:
                            answer.points_earned = question.points
                            earned_points += question.points
                answer.save()
            elif question.question_type == 'true_false':
                answer_text = request.POST.get(f'question_{question.id}')
                correct_choice = Choice.objects.filter(question=question, is_correct=True).first()
                if answer_text and correct_choice and answer_text == str(correct_choice.id):
                    answer.selected_choice = correct_choice
                    answer.is_correct = True
                    answer.points_earned = question.points
                    earned_points += question.points
                answer.save()
        
        # Calculate score
        attempt.score = earned_points
        attempt.percentage = int((earned_points / total_points * 100)) if total_points > 0 else 0
        attempt.passed = attempt.percentage >= attempt.quiz.passing_score
        attempt.completed_at = timezone.now()
        
        # Calculate time taken
        if attempt.quiz.time_limit_minutes > 0:
            time_diff = attempt.completed_at - attempt.started_at
            attempt.time_taken_minutes = int(time_diff.total_seconds() / 60)
        
        attempt.save()
        
        # Update enrollment progress if passed
        if attempt.passed:
            enrollment = Enrollment.objects.filter(user=request.user, course=attempt.quiz.course).first()
            if enrollment:
                enrollment.update_progress()
        
        messages.success(request, f'Quiz completed! Your score: {attempt.percentage}%')
        return redirect('quizzes:quiz_result', attempt_id=attempt.id)
    
    context = {
        'attempt': attempt,
        'questions': questions,
    }
    return render(request, 'quizzes/take_quiz.html', context)


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    answers = QuizAnswer.objects.filter(attempt=attempt).select_related('question', 'selected_choice')
    
    context = {
        'attempt': attempt,
        'answers': answers,
    }
    return render(request, 'quizzes/quiz_result.html', context)

