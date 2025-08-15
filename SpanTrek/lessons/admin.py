from django.contrib import admin
from .models import Lesson, UserLessonProgress


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'order', 'is_active', 'created_at']
    list_filter = ['level', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'level']


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'score', 'completed_at']
    list_filter = ['is_completed', 'lesson__level']
    search_fields = ['user__username', 'lesson__title']
    ordering = ['-completed_at']

