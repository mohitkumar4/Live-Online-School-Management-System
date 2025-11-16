from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('attempt/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
    path('attempt/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
]

