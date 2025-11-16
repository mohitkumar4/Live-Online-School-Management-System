from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/complete/', views.mark_complete, name='mark_complete'),
]

