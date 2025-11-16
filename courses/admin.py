from django.contrib import admin
from .models import Category, Course, CourseReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'difficulty_level', 'status', 'is_free', 'rating', 'created_at')
    list_filter = ('status', 'difficulty_level', 'is_free', 'category', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('total_enrollments', 'rating', 'total_ratings', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'instructor', 'category')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Course Details', {
            'fields': ('difficulty_level', 'language', 'duration_hours', 'learning_outcomes', 'requirements')
        }),
        ('Settings', {
            'fields': ('status', 'is_free', 'price', 'tags')
        }),
        ('Statistics', {
            'fields': ('total_enrollments', 'rating', 'total_ratings', 'total_lessons')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('course__title', 'user__username', 'comment')

