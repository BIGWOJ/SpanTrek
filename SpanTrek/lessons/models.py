from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Enums for different content types
class ContentType(models.TextChoices):
    VOCABULARY = 'vocabulary', 'Vocabulary'
    LISTENING = 'listening', 'Listening'
    READING = 'reading', 'Reading'

# Core content models
class Lesson(models.Model):
    """Main lesson container"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)  # For lesson ordering
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

class Word(models.Model):
    """Individual vocabulary words"""
    spanish_word = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200)
    pronunciation = models.CharField(max_length=200, blank=True)  # IPA or phonetic
    example_sentence_spanish = models.TextField(blank=True)
    example_sentence_english = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='words/audio/', blank=True, null=True)
    image = models.ImageField(upload_to='words/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['spanish_word', 'english_translation']
        ordering = ['spanish_word']

    def __str__(self):
        return f"{self.spanish_word} - {self.english_translation}"

class ListeningExercise(models.Model):
    """Listening comprehension exercises"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='listening/audio/')
    transcript = models.TextField()  # Full transcript for reference
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class ReadingPassage(models.Model):
    """Reading comprehension passages"""
    title = models.CharField(max_length=200)
    content = models.TextField()  # The text to read
    word_count = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

# Junction models connecting lessons to content
class LessonWord(models.Model):
    """Words included in a lesson"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_lessons')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['lesson', 'word']
        ordering = ['order']

class LessonListening(models.Model):
    """Listening exercises in a lesson"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_listenings')
    listening_exercise = models.ForeignKey(ListeningExercise, on_delete=models.CASCADE, related_name='listening_lessons')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['lesson', 'listening_exercise']
        ordering = ['order']

class LessonReading(models.Model):
    """Reading passages in a lesson"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_readings')
    reading_passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name='reading_lessons')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['lesson', 'reading_passage']
        ordering = ['order']

# User progress tracking models
class UserProgress(models.Model):
    """Overall user progress in lessons"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)  # Overall lesson score (0-100)
    started_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']

    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"{self.user.username} - {self.lesson.title} ({status})"

class UserWordKnowledge(models.Model):
    """Track which words a user knows"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='word_knowledge')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='user_knowledge')
    
    # Knowledge levels
    KNOWLEDGE_CHOICES = [
        ('unknown', 'Unknown'),
        ('learning', 'Learning'),
        ('familiar', 'Familiar'),
        ('known', 'Known'),
        ('mastered', 'Mastered'),
    ]
    knowledge_level = models.CharField(max_length=20, choices=KNOWLEDGE_CHOICES, default='unknown')
    
    # Spaced repetition data
    next_review_date = models.DateTimeField(default=timezone.now)
    review_count = models.PositiveIntegerField(default=0)
    correct_streak = models.PositiveIntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'word']

    def __str__(self):
        return f"{self.user.username} - {self.word.spanish_word} ({self.knowledge_level})"

class UserListeningProgress(models.Model):
    """Track user's listening exercise completions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_progress')
    listening_exercise = models.ForeignKey(ListeningExercise, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)  # Score (0-100)
    times_attempted = models.PositiveIntegerField(default=0)
    best_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'listening_exercise']

    def __str__(self):
        return f"{self.user.username} - {self.listening_exercise.title}"

class UserReadingProgress(models.Model):
    """Track user's reading passage completions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_progress')
    reading_passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)  # Score (0-100)
    times_read = models.PositiveIntegerField(default=0)
    reading_time_seconds = models.PositiveIntegerField(null=True, blank=True)  # Track reading speed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'reading_passage']

    def __str__(self):
        return f"{self.user.username} - {self.reading_passage.title}"

# Review and practice session models
class ReviewSession(models.Model):
    """Track review sessions for spaced repetition"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_sessions')
    session_type = models.CharField(max_length=20, choices=ContentType.choices)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_items = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    
    @property
    def accuracy(self):
        if self.total_items == 0:
            return 0
        return (self.correct_answers / self.total_items) * 100

    def __str__(self):
        return f"{self.user.username} - {self.session_type} review ({self.started_at.date()})"

class WordReview(models.Model):
    """Individual word review within a session"""
    session = models.ForeignKey(ReviewSession, on_delete=models.CASCADE, related_name='word_reviews')
    word_knowledge = models.ForeignKey(UserWordKnowledge, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        result = "✓" if self.is_correct else "✗"
        return f"{result} {self.word_knowledge.word.spanish_word}"
