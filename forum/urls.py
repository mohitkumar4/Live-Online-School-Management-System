from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('course/<slug:course_slug>/', views.discussion_list, name='discussion_list'),
    path('course/<slug:course_slug>/create/', views.create_discussion, name='create_discussion'),
    path('<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('reply/<int:reply_id>/mark-answer/', views.mark_as_answer, name='mark_as_answer'),
]

