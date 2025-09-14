from django.db import models
from django.conf import settings
from django.utils import timezone


class Country(models.Model):
    """Countries for organizing lessons (e.g., Spain, Peru, Chile)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Landmark(models.Model):
    """Places within countries (e.g., Madrid, Warsaw, Macchu Picchu)"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='landmarks')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('country', 'name')
        ordering = ['country', 'name']

    def __str__(self):
        return f"{self.name}, {self.country.name}"


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


class ContentTypeChoices(models.TextChoices):
    """Content types for adventure lesson content blocks"""
    TEXT = 'text', 'Text'
    IMAGE = 'image', 'Image'
    VIDEO = 'video', 'Video'
    AUDIO = 'audio', 'Audio'


class Lesson(models.Model):
    """Spanish lessons organized by city"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField()
    city = models.CharField(max_length=50)  # e.g., szczecin, krakow, etc.
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    vocabularies = models.ManyToManyField('Vocabulary', blank=True, related_name='lessons')
    sentences = models.ManyToManyField('Sentence', blank=True, related_name='lessons')

    class Meta:
        ordering = ['city', 'order']
        unique_together = ('city', 'order')

    def __str__(self):
        return f"{self.city.title()} - {self.title}"


class AdventureLessonContent(models.Model):
    """Individual content blocks within a adventure lesson"""

    lesson = models.ForeignKey(AdventureLesson, on_delete=models.CASCADE, related_name='content_blocks')
    content_id = models.AutoField(primary_key=True, help_text="Unique content block identifier")
    content_type = models.CharField(max_length=20, choices=ContentTypeChoices.choices, default='text')
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
    
    # Scoring
    score = models.IntegerField(default=0)  # Total points earned
    max_score = models.IntegerField(default=0)  # Maximum possible points
 
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)
    
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
            self.time_spent = timezone.now() - self.started_at

            # Award experience points to user
            self.user.experience += self.lesson.experience_points
            self.user.save()
            
            self.save()
            return True
        return False


class Vocabulary(models.Model):
    """Vocabulary words introduced in lessons"""
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=150, blank=True)
    example_sentence = models.TextField(blank=True)
    conjugation = models.TextField(blank=True)
    
    # Audio
    audio_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Vocabulary"
        ordering = ['word']

    def __str__(self):
        return f"{self.word} - {self.translation}"
    
    
class Sentence(models.Model):
    """Example sentences"""
    sentence = models.TextField()
    translation = models.TextField()

    class Meta:
        ordering = ['sentence']

    def __str__(self):
        return f"{self.sentence} - {self.translation}"


