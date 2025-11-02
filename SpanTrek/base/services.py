"""
Achievement service for handling achievement logic
"""
from .models import User, Achievement, UserAchievement

class AchievementService:
    """Service class to handle achievement checking and awarding"""
    
    @staticmethod
    def check_and_award_achievements(user):
        """Check all possible achievements for a user and award them if conditions are met"""
        achievements_awarded = []
        
        # First Steps - Complete first lesson (has experience > 0)
        if user.experience > 0 and not user.has_achievement('First Steps'):
            if user.award_achievement('First Steps'):
                achievements_awarded.append('First Steps')
        
        # Getting Started - Earn 100 experience points
        if user.experience >= 100 and not user.has_achievement('Getting Started'):
            if user.award_achievement('Getting Started'):
                achievements_awarded.append('Getting Started')
        
        # Experience Hunter - Earn 1000 experience points
        if user.experience >= 1000 and not user.has_achievement('Experience Hunter'):
            if user.award_achievement('Experience Hunter'):
                achievements_awarded.append('Experience Hunter')
        
        # Experience Master - Earn 5000 experience points
        if user.experience >= 5000 and not user.has_achievement('Experience Master'):
            if user.award_achievement('Experience Master'):
                achievements_awarded.append('Experience Master')
        
        # Streak Beginner - 3 days streak
        if user.days_streak >= 3 and not user.has_achievement('Streak Beginner'):
            if user.award_achievement('Streak Beginner'):
                achievements_awarded.append('Streak Beginner')
        
        # Streak Master - 7 days streak
        if user.days_streak >= 7 and not user.has_achievement('Streak Master'):
            if user.award_achievement('Streak Master'):
                achievements_awarded.append('Streak Master')
        
        # Streak Legend - 30 days streak
        if user.days_streak >= 30 and not user.has_achievement('Streak Legend'):
            if user.award_achievement('Streak Legend'):
                achievements_awarded.append('Streak Legend')
        
        # Dedicated Student - 30 days streak (same as streak legend for simplicity)
        if user.days_streak >= 30 and not user.has_achievement('Dedicated Student'):
            if user.award_achievement('Dedicated Student'):
                achievements_awarded.append('Dedicated Student')
        
        # Level Up - Reach level 5
        if user.level >= 5 and not user.has_achievement('Level Up'):
            if user.award_achievement('Level Up'):
                achievements_awarded.append('Level Up')
        
        # Expert - Reach level 10
        if user.level >= 10 and not user.has_achievement('Expert'):
            if user.award_achievement('Expert'):
                achievements_awarded.append('Expert')
        
        # Master - Reach level 20
        if user.level >= 20 and not user.has_achievement('Master'):
            if user.award_achievement('Master'):
                achievements_awarded.append('Master')
        
        # Adventure Starter - Make progress in adventure
        if user.adventure_progress > 0 and not user.has_achievement('Adventure Starter'):
            if user.award_achievement('Adventure Starter'):
                achievements_awarded.append('Adventure Starter')
        
        # Adventure Explorer - Complete 50% of adventure (assuming 100 is full completion)
        if user.adventure_progress >= 50 and not user.has_achievement('Adventure Explorer'):
            if user.award_achievement('Adventure Explorer'):
                achievements_awarded.append('Adventure Explorer')
        
        # Adventure Hero - Complete adventure (assuming 100 is full completion)
        if user.adventure_progress >= 100 and not user.has_achievement('Adventure Hero'):
            if user.award_achievement('Adventure Hero'):
                achievements_awarded.append('Adventure Hero')
        
        return achievements_awarded
    
    @staticmethod
    def get_user_achievements_status_exp(user):
        """Get all achievements with status (earned/not earned) for a specific user"""
        all_achievements = Achievement.objects.all()
        user_earned_achievements = set(
            user.earned_achievements.values_list('achievement__name', flat=True)
        )
        
        achievements_data = []
        for achievement in all_achievements:
            achievements_data.append({
                'achievement': achievement,
                'earned': achievement.name in user_earned_achievements,
                'experience_award': achievement.experience_award,
            })

        return sorted(achievements_data, key=lambda exp: exp['experience_award'], reverse=True)

    @staticmethod
    def award_manual_achievement(user, achievement_name):
        """Manually award an achievement (for admin or special cases)"""
        return user.award_achievement(achievement_name)
