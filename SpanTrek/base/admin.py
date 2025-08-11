from django.contrib import admin
from .models import User, Achievement, UserAchievement

class UserAchievementInline(admin.TabularInline):
    model = UserAchievement
    extra = 0
    readonly_fields = ('earned_at',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'level', 'experience', 'days_streak', 'achievement_count']
    list_filter = ['level', 'days_streak']
    search_fields = ['username', 'email']
    inlines = [UserAchievementInline]
    
    def achievement_count(self, obj):
        return obj.achievements.count()
    achievement_count.short_description = 'Achievements'

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'condition_type', 'condition_value', 'users_earned']
    list_filter = ['condition_type', 'is_hidden']
    search_fields = ['name', 'description']
    
    def users_earned(self, obj):
        return UserAchievement.objects.filter(achievement=obj).count()
    users_earned.short_description = 'Users Earned'

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['earned_at']
    search_fields = ['user__username', 'achievement__name']
