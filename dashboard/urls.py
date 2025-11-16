from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('instructor-courses/', views.instructor_courses, name='instructor_courses'),
]

