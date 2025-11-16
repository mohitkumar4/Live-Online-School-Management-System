from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('generate/<slug:course_slug>/', views.generate_certificate, name='generate_certificate'),
    path('<str:certificate_number>/', views.certificate_detail, name='certificate_detail'),
    path('', views.my_certificates, name='my_certificates'),
]

