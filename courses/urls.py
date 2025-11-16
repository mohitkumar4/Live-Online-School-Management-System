from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:slug>/edit/', views.course_edit, name='course_edit'),
    path('<slug:slug>/review/', views.add_review, name='add_review'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]

