from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
from datetime import date
from lessons.models import Lesson

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    avatar = models.ImageField(default='avatars/default_avatar.png', upload_to='avatars/', null=True, blank=True)

    days_streak = models.IntegerField(default=0)
    highest_streak = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    adventure_progress = models.IntegerField(default=0)
    words_learned = models.JSONField(default=list, blank=True) # Store list of learned words
    sentences_learned = models.JSONField(default=list, blank=True) # Store list of learned sentences
    audio_learned = models.JSONField(default=list, blank=True) # Store list of learned audio clips
    use_of_spanish = models.IntegerField(default=0)  # Use of Spanish 
    activity_days = models.JSONField(default=list, blank=True)  # Store list of active dates as strings
    last_activity_date = models.DateField(null=True, blank=True)  # Track last activity for streak calculation
    passports_earned = models.JSONField(default=list, blank=True)  # Store list of earned passports

    # Default numbers of practice questions 
    default_random_practice_count = models.IntegerField(default=20)  
    default_vocabulary_practice_count = models.IntegerField(default=20)
    default_sentence_practice_count = models.IntegerField(default=10)
    default_listening_practice_count = models.IntegerField(default=10)

    # Country lessons progress tracking
    country_lessons_progress = models.JSONField(default=dict, blank=True)  # e.g., {"Spain": 3, "Mexico": 5}
    
    landmark_lessons_progress = models.JSONField(default=dict, blank=True)  # e.g., {"Madrid": 2, "Warsaw": 4}
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def update_progress_after_lesson(self, landmark, lesson_number):
        if self.is_authenticated:
            if self.last_activity_date != date.today():
                self.mark_activity_today()
                self.calculate_streak()
            
            if self.landmark_lessons_progress.get(landmark, -1) >= lesson_number:
                return  # No update needed if lesson already completed or in progress
            self.experience += 50
            self.adventure_progress += 1

            lesson = Lesson.objects.filter(landmark=landmark, order=lesson_number).first()

            # Add new words to user's learned words list
            lesson_words = set(vocab.word for vocab in lesson.vocabularies.all())
            # Ensure words_learned is a list (safety check)
            if not isinstance(self.words_learned, list):
                self.words_learned = []
            new_words = lesson_words - set(self.words_learned)
            self.words_learned.extend(new_words)

            # Add new sentences to user's learned sentences list
            lesson_sentences = set(sentence.sentence for sentence in lesson.sentences.all()) 
            # Ensure sentences_learned is a list (safety check)
            if not isinstance(self.sentences_learned, list):
                self.sentences_learned = []
            new_sentences = lesson_sentences - set(self.sentences_learned)
            self.sentences_learned.extend(new_sentences)

            # Update country progress (increment by 1, but don't exceed total lessons)
            country_lessons_counter = Lesson.objects.filter(country=lesson.country).count()

            current_progress = self.country_lessons_progress.get(lesson.country.name, 0)
            self.country_lessons_progress[lesson.country.name] = min(
                current_progress + 1, 
                country_lessons_counter
            )
            
            self.landmark_lessons_progress[landmark] = max(
                self.landmark_lessons_progress.get(landmark, 0), 
                lesson_number + 1
            )

            self.save()

    def update_progress_after_practice(self):
        print(date.today())
        print(self.last_activity_date)
        
        if self.is_authenticated:
            if self.last_activity_date != date.today():
                print('aaa')
                self.mark_activity_today()
                self.calculate_streak()
            
            self.experience += 20
            self.save()

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
            self.calculate_streak()
            self.save()
            print('bbbbbb')

    def calculate_streak(self):
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
        
        # Update highest streak if needed
        highest_streak = self.highest_streak
        if current_streak > highest_streak:
            self.highest_streak = current_streak


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

