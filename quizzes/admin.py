from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, QuizAnswer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'passing_score', 'time_limit_minutes', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'course__title')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'points', 'order')
    list_filter = ('question_type', 'quiz')
    search_fields = ('question_text', 'quiz__title')
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'is_correct', 'order')
    list_filter = ('is_correct',)
    search_fields = ('choice_text', 'question__question_text')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'percentage', 'passed', 'started_at', 'completed_at')
    list_filter = ('passed', 'started_at')
    search_fields = ('user__username', 'quiz__title')


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct', 'points_earned')
    list_filter = ('is_correct',)
    search_fields = ('attempt__user__username', 'question__question_text')

