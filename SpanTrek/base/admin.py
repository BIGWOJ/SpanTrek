from django.contrib import admin
from .models import User, Achievement, UserAchievement

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'level', 'experience', 'days_streak']
    list_filter = ['level', 'days_streak']
    search_fields = ['username', 'email']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'experience_award', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement']
    list_filter = ['achievement']
    search_fields = ['user__username', 'achievement__name']
