from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
from datetime import date
from lessons.models import Landmark, Lesson
from practice.models import DailyChallenge
from .services import AchievementService
import random


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    avatar = models.ImageField(default='avatars/default_avatar.png', upload_to='avatars/', null=True, blank=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    adventure_progress = models.IntegerField(default=0)
    passports_earned = models.JSONField(default=list, blank=True)
    
    # Knowledge
    words_learned = models.JSONField(default=list, blank=True)
    sentences_learned = models.JSONField(default=list, blank=True)
    audio_learned = models.JSONField(default=list, blank=True)
    use_of_spanish = models.IntegerField(default=0)
    
    # Activity 
    days_streak = models.IntegerField(default=0)
    highest_streak = models.IntegerField(default=0)
    activity_days = models.JSONField(default=list, blank=True)
    last_activity_date = models.DateField(null=True, blank=True)

    # Default numbers of practice questions 
    default_random_practice_count = models.IntegerField(default=20)  
    default_vocabulary_practice_count = models.IntegerField(default=20)
    default_sentence_practice_count = models.IntegerField(default=10)
    default_listening_practice_count = models.IntegerField(default=10)

    # Country/landmark lessons progress tracking
    country_lessons_progress = models.JSONField(default=dict, blank=True)  # e.g., {"spain": 3, "mexico": 5}
    landmark_lessons_progress = models.JSONField(default=dict, blank=True)  # e.g., {"madrid": 2, "warsaw": 4}
    
    # Daily challenges
    daily_challenges = models.JSONField(default=list, blank=True)
    daily_challenges_creation_date = models.DateField(null=True, blank=True)
    daily_challenges_completed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def update_progress_after_lesson(self, landmark, lesson_number, lesson_completed_before=False):
        if self.is_authenticated:
            if self.last_activity_date != date.today():
                self.mark_activity_today()
                self.calculate_streak()

            if self.landmark_lessons_progress.get(landmark, -1) >= lesson_number+1:
                self.experience += 50
                self.save()
                # No more updates needed if lesson already completed
                return
            self.experience += 100
            
            if not lesson_completed_before:
                self.adventure_progress += 1

            landmark_obj = Landmark.objects.filter(name=landmark).first()
            lesson = Lesson.objects.filter(landmark=landmark_obj, order=lesson_number).first()

            # Add knowledge from lesson to user's learned lists
            # Words
            lesson_words = set(vocab.word for vocab in lesson.vocabularies.all())
            if not isinstance(self.words_learned, list):
                self.words_learned = []
            new_words = lesson_words - set(self.words_learned)
            self.words_learned.extend(new_words)

            # Sentences
            lesson_sentences = set(sentence.sentence for sentence in lesson.sentences.all()) 
            if not isinstance(self.sentences_learned, list):
                self.sentences_learned = []
            new_sentences = lesson_sentences - set(self.sentences_learned)
            self.sentences_learned.extend(new_sentences)

            # Audio files
            lesson_audios = set(audio.text for audio in lesson.audios.all())
            if not isinstance(self.audio_learned, list):
                self.audio_learned = []
            new_audios = lesson_audios - set(self.audio_learned)
            self.audio_learned.extend(new_audios)
            
            # Use of Spanish
            self.use_of_spanish += lesson.use_of_spanish

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

            self.progress_daily_challenges(lesson=lesson)
            self.save()

    def update_progress_after_practice(self, practice_type):
        if self.is_authenticated:
            if self.last_activity_date != date.today():
                self.mark_activity_today()
                self.calculate_streak()
            
            self.experience += 25
            self.progress_daily_challenges(practice_type=practice_type)
            self.save()

    def has_achievement(self, achievement_name):
        """Check if user has earned a specific achievement by name"""
        return self.earned_achievements.filter(achievement__name=achievement_name).exists()

    def award_achievement(self, achievement_name):
        """Award and add an achievement to the user"""
        achievement_obj = Achievement.objects.filter(name=achievement_name).first()
        if achievement_obj:
            # Check if user already has this achievement to prevent duplicates
            if self.earned_achievements.filter(achievement=achievement_obj).exists():
                return False  # Achievement already earned
                
            self.experience += achievement_obj.experience_award
            new_user_achievement = UserAchievement.objects.create(
                user=self,
                achievement=achievement_obj
            )
            self.check_if_new_level()
            self.save()
            return True
        else:
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
        if current_streak > self.highest_streak:
            self.highest_streak = current_streak

    def create_daily_challenges(self):
        all_challenges = list(DailyChallenge.objects.all())
        daily_challenges_count = 3
        selected_challenges = random.sample(all_challenges, k=daily_challenges_count)
                
        self.daily_challenges = [
            {
                'code': challenge.code,
                'description': challenge.description,
                'progress': 0,
                'max_progress': challenge.max_progress,
                'completed': False
            }
            for challenge in selected_challenges
        ]
        self.daily_challenges_completed = False
        
        self.save()
        
    def check_if_new_level(self):
        if self.experience >= self.level * 500:
            self.level += 1
            self.save()
        
    def progress_daily_challenges(self, practice_type=None, lesson=None):
        # Map practice types to challenge prefixes
        practice_prefixes = {
            'random': ('RP', 'P'),
            'vocabulary': ('VP', 'P'), 
            'sentence': ('SP', 'P'),
            'listening': ('LP', 'P')
        }
        
        # Get prefixes if practice_type is provided and valid
        prefixes = practice_prefixes.get(practice_type, ()) if practice_type else ()
        
        for challenge in self.daily_challenges:
            # Experience points challenge
            if challenge['code'].startswith('EX') and not challenge['completed']:
                if lesson is not None:
                    challenge['progress'] += 100
                elif practice_type in practice_prefixes.keys():
                    challenge['progress'] += 25
                
            # Complete lessons challenge
            if challenge['code'].startswith('C') and not challenge['completed']:
                challenge['progress'] += 1

            # Practice challenges
            if not challenge['completed'] and prefixes and challenge['code'].startswith(prefixes):
                challenge['progress'] += 1

            # Learn new (vocabularies/sentences/audios) / complete lessons challenge
            if lesson is not None and challenge['code'].startswith(('C', 'NW', 'NS', 'NA')) and not challenge['completed']:
                if challenge['code'].startswith('NW'):
                    challenge['progress'] += lesson.vocabularies.count()
                elif challenge['code'].startswith('NS'):
                    challenge['progress'] += lesson.sentences.count()
                elif challenge['code'].startswith('NA'):
                    challenge['progress'] += lesson.audios.count()

            # Check if challenge is completed
            if challenge['progress'] >= challenge['max_progress']:
                    challenge['completed'] = True
        
        # Check if all challenges are completed and award bonus XP
        if not self.daily_challenges_completed:
            completed_count = sum(1 for challenge in self.daily_challenges if challenge['completed'])
            if completed_count == len(self.daily_challenges):
                self.experience += 75
                self.daily_challenges_completed = True
               
        self.check_if_new_level()
        AchievementService.check_and_award_achievements(self)
        self.save()


class Achievement(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    experience_award = models.IntegerField(default=0)

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
        # Prevent duplicate achievements
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

