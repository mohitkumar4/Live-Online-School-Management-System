"""
URL configuration for liveSchool project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('lessons/', include('lessons.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('certificates/', include('certificates.urls')),
    path('forum/', include('forum.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('courses.urls')),  # Keep this last as it matches root and all other paths
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

