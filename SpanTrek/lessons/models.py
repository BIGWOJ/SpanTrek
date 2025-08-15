from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Country(models.Model):
    """Countries for organizing lessons (e.g., Spain, Peru, Chile)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AdventureLesson(models.Model):
    """Main lesson model"""
    
    lesson_id = models.AutoField(primary_key=True, help_text="Auto-incrementing lesson identifier")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    
    # Gamification
    experience_points = models.IntegerField(default=10)
    required_score = models.IntegerField(default=75, help_text="Minimum score to pass (percentage)")

    class Meta:
        ordering = ['country', 'order']

    def __str__(self):
        return f"Lesson {self.lesson_id}: {self.country.name} - Order {self.order}"


class ContentType(models.TextChoices):
    """Content types for adventure lesson content blocks"""
    TEXT = 'text', 'Text'
    IMAGE = 'image', 'Image'
    VIDEO = 'video', 'Video'
    AUDIO = 'audio', 'Audio'
    

class AdventureLessonContent(models.Model):
    """Individual content blocks within a adventure lesson"""

    lesson = models.ForeignKey(AdventureLesson, on_delete=models.CASCADE, related_name='content_blocks')
    content_id = models.AutoField(primary_key=True, help_text="Unique content block identifier")
    content_type = models.CharField(max_length=20, choices=ContentType.choices, default='text')
    title = models.CharField(max_length=200, blank=True)
    content_text = models.TextField(null=True, blank=True, help_text="Main content text for the lesson")
    media_url = models.URLField(blank=True, null=True, help_text="URL for images, audio, or video")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"{self.lesson.lesson_id} - {self.content_id}: {self.content_type.title()}"


class Exercise(models.Model):
    """Exercises within lessons"""
    EXERCISE_TYPES = [
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('fill_blank', 'Fill in the Blank'),
        ('matching', 'Matching'),
        ('translation', 'Translation'),
        ('audio_comprehension', 'Audio Comprehension'),
        ('speaking', 'Speaking Practice'),
    ]
    
    lesson = models.ForeignKey(AdventureLesson, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=30, choices=EXERCISE_TYPES)
    question = models.TextField()
    instructions = models.TextField(blank=True)
    
    # Answer data (stored as JSON for flexibility)
    correct_answers = models.JSONField(help_text="Correct answer(s) - format depends on exercise type")
    choices = models.JSONField(default=list, blank=True, help_text="Multiple choice options")
    
    # Metadata
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=1)
 
    class Meta:
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"Lesson {self.lesson.lesson_id} - Exercise {self.order}"


class UserLessonProgress(models.Model):
    """Track user progress through lessons"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(AdventureLesson, on_delete=models.CASCADE, related_name='user_progress')
    
    # Progress tracking
    is_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    current_exercise = models.IntegerField(default=0)  # Track which exercise user is on
    
    # Scoring
    score = models.IntegerField(default=0)  # Total points earned
    max_score = models.IntegerField(default=0)  # Maximum possible points
    attempts = models.IntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'lesson')
    
    def __str__(self):
        return f"{self.user.username} - Lesson {self.lesson.lesson_id}"
    
    @property
    def percentage_score(self):
        """Calculate percentage score"""
        if self.max_score == 0:
            return 0
        return round((self.score / self.max_score) * 100)
    
    def mark_started(self):
        """Mark lesson as started"""
        if not self.is_started:
            self.is_started = True
            self.started_at = timezone.now()
            self.save()
    
    def mark_completed(self):
        """Mark lesson as completed if score meets requirement"""
        if not self.is_completed and self.percentage_score >= self.lesson.required_score:
            self.is_completed = True
            self.completed_at = timezone.now()
            
            # Award experience points to user
            self.user.experience += self.lesson.experience_points
            self.user.save()
            
            self.save()
            return True
        return False


class UserExerciseAttempt(models.Model):
    """Track individual exercise attempts"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='attempts')
    
    # Attempt data
    user_answer = models.JSONField()  # User's answer - format depends on exercise type
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    
    # Metadata
    attempt_number = models.IntegerField(default=1)
    time_taken = models.IntegerField(default=0, help_text="Time taken in seconds")
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-attempted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise} - Attempt {self.attempt_number}"


class Vocabulary(models.Model):
    """Vocabulary words introduced in lessons"""
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=150, blank=True)
    definition = models.TextField(blank=True)
    example_sentence = models.TextField(blank=True)
    lesson = models.ForeignKey(AdventureLesson, on_delete=models.CASCADE, related_name='vocabulary')
    
    # Audio
    audio_url = models.URLField(blank=True)
    
    # Metadata
    difficulty_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Vocabulary"
        ordering = ['lesson', 'word']
    
    def __str__(self):
        return f"{self.word} - {self.translation}"


class UserVocabularyProgress(models.Model):
    """Track user's vocabulary learning progress"""
    MASTERY_LEVELS = [
        ('learning', 'Learning'),
        ('practiced', 'Practiced'),
        ('mastered', 'Mastered'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    mastery_level = models.CharField(max_length=20, choices=MASTERY_LEVELS, default='learning')
    
    # Progress tracking
    times_seen = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'vocabulary')
        verbose_name_plural = "User Vocabulary Progress"
    
    def __str__(self):
        return f"{self.user.username} - {self.vocabulary.word}"
    
    @property
    def accuracy_rate(self):
        """Calculate accuracy rate"""
        if self.times_seen == 0:
            return 0
        return round((self.times_correct / self.times_seen) * 100)
