from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
from datetime import date

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)

    days_streak = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    adventure_progress = models.IntegerField(default=0)
    words_learned = models.IntegerField(default=0)
    activity_days = models.JSONField(default=list, blank=True)  # Store list of active dates as strings
    last_activity_date = models.DateField(null=True, blank=True)  # Track last activity for streak calculation 

    # Country lessons progress tracking
    country_lessons_progress = models.JSONField(default=dict, blank=True)  # e.g., {"Spain": 3, "Mexico": 5}
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_achievement(self, achievement_name):
        """Check if user has earned a specific achievement by name"""
        return self.earned_achievements.filter(achievement__name=achievement_name).exists()

    def award_achievement(self, achievement_name):
        """Award an achievement to the user if they don't already have it"""
        try:
            achievement = Achievement.objects.get(name=achievement_name)
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=self,
                achievement=achievement
            )
            if created:
                # Award experience points
                self.experience += achievement.experience_award
                self.save()
                return True
        except Achievement.DoesNotExist:
            pass
        return False

    def mark_activity_today(self):
        """Mark today as an active day and update streak"""
        today = date.today()
        today_str = today.isoformat()
        
        # Don't add duplicate entries for the same day
        if today_str not in self.activity_days:
            self.activity_days.append(today_str)
            self.last_activity_date = today
            self._calculate_streak()
            self.save()
            return True
        return False

    def _calculate_streak(self):
        """Calculate current streak based on activity_days"""
        if not self.activity_days:
            self.days_streak = 0
            return
        
        # Sort dates and convert to date objects
        sorted_dates = sorted([date.fromisoformat(d) for d in self.activity_days])
        today = date.today()
        
        # Start from today and count backwards
        current_streak = 0
        current_date = today
        
        # Check if today is in the activity list
        if today.isoformat() in self.activity_days:
            current_streak = 1
            current_date = today
        elif len(sorted_dates) > 0 and sorted_dates[-1] == today - timezone.timedelta(days=1):
            # If last activity was yesterday, start streak from yesterday
            current_date = sorted_dates[-1]
            current_streak = 1
        else:
            # No recent activity, streak is 0
            self.days_streak = 0
            return
        
        # Count backwards from current_date
        for i in range(len(sorted_dates) - 1, -1, -1):
            expected_date = current_date - timezone.timedelta(days=current_streak - 1)
            if sorted_dates[i] == expected_date:
                if i == 0:  # First element, no more to check
                    break
                # Check if previous day exists
                prev_expected = expected_date - timezone.timedelta(days=1)
                if i > 0 and sorted_dates[i - 1] == prev_expected:
                    current_streak += 1
                else:
                    break
            else:
                break
        
        self.days_streak = current_streak


class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Use name as unique identifier
    description = models.TextField()
    icon = models.CharField(max_length=50)
    experience_award = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)  # To enable/disable achievements

    # Many-to-many relationship with User through UserAchievement
    users = models.ManyToManyField(User, through='UserAchievement', related_name='achievements')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def slug(self):
        """Generate slug from name for compatibility"""
        return slugify(self.name)


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='earned_by')
 
    class Meta:
        unique_together = ('user', 'achievement')  # Prevent duplicate achievements

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

