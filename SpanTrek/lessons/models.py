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
    adventure_order = models.IntegerField(default=1)


    class Meta:
        unique_together = ('country', 'name')
        ordering = ['country', 'name']

    def __str__(self):
        return f"{self.country.name}, {self.name}"


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


class Lesson(models.Model):
    """Spanish lessons organized by landmark"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField()
    adventure_order = models.IntegerField(default=1)
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='lessons')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    vocabularies = models.ManyToManyField('Vocabulary', blank=True, related_name='lessons')
    sentences = models.ManyToManyField('Sentence', blank=True, related_name='lessons')
    audios = models.ManyToManyField('Audio', blank=True, related_name='lessons')
    use_of_spanish = models.IntegerField(default=0, help_text="Number of use of Spanish exercises in the lesson")
    lesson_sequence = models.JSONField(default=list, blank=True, help_text="Sequence of content types in the lesson")

    class Meta:
        ordering = ['landmark', 'order']
        unique_together = ('landmark', 'order')

    def __str__(self):
        return f"{self.landmark.name.title()} - {self.title}"


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


class Audio(models.Model):
    """Audio clips for listening"""
    audio_url = models.CharField(max_length=200)
    text = models.TextField(max_length=500, default="")

    class Meta:
        ordering = ['text']

    def __str__(self):
        return self.text
    
