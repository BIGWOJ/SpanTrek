"""
Achievement service for handling achievement logic
"""
from lessons.models import Lesson, Country
from datetime import date, datetime
from django.db import models

class AchievementService:
    """Service class to handle achievement checking and awarding"""
    
    @staticmethod
    def check_and_award_achievements(user):
        """Check all possible achievements for a user and award them if conditions are met"""
        
        # Level-based
        if user.level >= 2 and not user.has_achievement('Baby Step'):
            user.award_achievement('Baby Step')

        if user.level >= 5 and not user.has_achievement('Level Up'):
            user.award_achievement('Level Up')

        if user.level >= 10 and not user.has_achievement('Expert'):
            user.award_achievement('Expert')

        if user.level >= 20 and not user.has_achievement('Master'):
            user.award_achievement('Master')

        # Experience-based
        if user.experience >= 250 and not user.has_achievement('Getting Started'):
            user.award_achievement('Getting Started')

        if user.experience >= 2500 and not user.has_achievement('Experience Seeker'):
            user.award_achievement('Experience Seeker')

        if user.experience >= 5000 and not user.has_achievement('Experience Master'):
            user.award_achievement('Experience Master')

        # Streak-based
        if user.days_streak >= 3 and not user.has_achievement('Streak Beginner'):
            user.award_achievement('Streak Beginner')

        if user.days_streak >= 7 and not user.has_achievement('Streak Master'):
            user.award_achievement('Streak Master')

        if user.days_streak >= 30 and not user.has_achievement('Streak Legend'):
            user.award_achievement('Streak Legend')

        # Adventure-based
        if user.adventure_progress >= 1 and not user.has_achievement('Adventure Hero'):
            user.award_achievement('Adventure Hero')

        # Knowledge-based
        if len(user.words_learned) >= 100 and not user.has_achievement('Word Master'):
            user.award_achievement('Word Master')
        
        if len(user.sentences_learned) >= 25 and not user.has_achievement('Sentence Master'):
            user.award_achievement('Sentence Master')

        if len(user.audio_learned) >= 25 and not user.has_achievement('Audiofile'):
            user.award_achievement('Audiofile')
            
        total_use_of_spanish = Lesson.objects.aggregate(total=models.Sum('use_of_spanish'))['total'] or 0
        use_of_spanish_percentage = (user.use_of_spanish / total_use_of_spanish * 100) if total_use_of_spanish > 0 else 0
        if use_of_spanish_percentage >= 50 and not user.has_achievement('Spanish User'):
            user.award_achievement('Spanish User')

        # Time-based
        current_hour = datetime.now().hour
        if user.last_activity_date == date.today() and not user.has_achievement('Early Bird') and current_hour < 10:
            user.award_achievement('Early Bird')
        
        if user.last_activity_date == date.today() and not user.has_achievement('Night Owl') and current_hour >= 22:
            user.award_achievement('Night Owl')

        # Country-specific achievements
        poland_progress = user.country_lessons_progress.get('poland', 0)
        spain_progress = user.country_lessons_progress.get('spain', 0)
        
        # Get total lessons for each country
        poland_country = Country.objects.filter(name__iexact='poland').first()
        spain_country = Country.objects.filter(name__iexact='spain').first()

        total_poland_lessons = Lesson.objects.filter(country=poland_country).count()
        if total_poland_lessons > 0:
            poland_percentage = (poland_progress / total_poland_lessons) * 100
            
            if poland_percentage >= 50 and not user.has_achievement('Poland Explorer'):
                user.award_achievement('Poland Explorer')

            if poland_percentage >= 100 and not user.has_achievement('Poland Master'):
                user.award_achievement('Poland Master')
        
        total_spain_lessons = Lesson.objects.filter(country=spain_country).count()
        if total_spain_lessons > 0:
            spain_percentage = (spain_progress / total_spain_lessons) * 100
            
            if spain_percentage >= 50 and not user.has_achievement('Spain Explorer'):
                user.award_achievement('Spain Explorer')
            
            if spain_percentage >= 100 and not user.has_achievement('Spain Master'):
                user.award_achievement('Spain Master')
    
    
    @staticmethod
    def get_user_achievements_status_exp(user):
        """Get all achievements with status (earned/not earned) for a specific user"""
        # Importing here to avoid circular import
        from base.models import Achievement
        
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
