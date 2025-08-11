from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)

    days_streak = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    adventure_progress = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_user_achievements(self):
        """Get all achievements earned by this user"""
        return UserAchievement.objects.filter(user=self).select_related('achievement')

    def has_achievement(self, achievement_id):
        """Check if user has a specific achievement"""
        return UserAchievement.objects.filter(user=self, achievement_id=achievement_id).exists()

    def award_achievement(self, achievement):
        """Award an achievement to the user if they don't already have it"""
        user_achievement, created = UserAchievement.objects.get_or_create(
            user=self,
            achievement=achievement
        )
        return created  # Returns True if achievement was newly awarded

    def check_and_award_achievements(self):
        """Check all achievements and award any that the user qualifies for"""
        achievements_to_check = Achievement.objects.all()
        newly_awarded = []
        
        for achievement in achievements_to_check:
            if not self.has_achievement(achievement.id) and achievement.check_condition(self):
                if self.award_achievement(achievement):
                    newly_awarded.append(achievement)
        
        return newly_awarded


class Achievement(models.Model):
    CONDITION_TYPES = [
        ('experience', 'Experience Points'),
        ('level', 'Level'),
        ('streak', 'Days Streak'),
        ('adventure_progress', 'Adventure Progress'),
        ('custom', 'Custom Logic'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='⭐')  # Unicode emoji or icon
    
    # Condition settings
    condition_type = models.CharField(max_length=20, choices=CONDITION_TYPES)
    condition_value = models.IntegerField(help_text="Target value for the condition")
    
    # Achievement metadata
    points_reward = models.IntegerField(default=10, help_text="XP bonus for earning this achievement")
    is_hidden = models.BooleanField(default=False, help_text="Hidden until earned")
 
    class Meta:
        ordering = ['condition_value', 'name']

    def __str__(self):
        return self.name

    def check_condition(self, user):
        """Check if user meets the condition for this achievement"""
        if self.condition_type == 'experience':
            return user.experience >= self.condition_value
        elif self.condition_type == 'level':
            return user.level >= self.condition_value
        elif self.condition_type == 'streak':
            return user.days_streak >= self.condition_value
        elif self.condition_type == 'adventure_progress':
            return user.adventure_progress >= self.condition_value
        elif self.condition_type == 'custom':
            # For custom achievements, you can add specific logic here
            return self._check_custom_condition(user)
        return False

    def _check_custom_condition(self, user):
        """Override this method for custom achievement logic"""
        # Example custom conditions:
        if self.name == "Well Rounded":
            # Requires user to have at least level 3 AND 5+ day streak
            return user.level >= 3 and user.days_streak >= 5
        elif self.name == "Perfectionist":
            # Requires user to have exactly matching level and streak
            return user.level == user.days_streak and user.level >= 10
        
        return False


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"