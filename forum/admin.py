from django.contrib import admin
from .models import Discussion, DiscussionReply, Comment


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'user', 'is_pinned', 'views', 'created_at')
    list_filter = ('is_pinned', 'created_at', 'course')
    search_fields = ('title', 'content', 'user__username', 'course__title')
    list_editable = ('is_pinned',)


@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'user', 'is_answer', 'created_at')
    list_filter = ('is_answer', 'created_at')
    search_fields = ('content', 'user__username', 'discussion__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'lesson__title')

