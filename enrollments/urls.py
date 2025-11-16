from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('enroll/<slug:slug>/', views.enroll, name='enroll'),
    path('unenroll/<slug:slug>/', views.unenroll, name='unenroll'),
]

