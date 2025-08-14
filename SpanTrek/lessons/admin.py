from django.contrib import admin
from .models import (
    Lesson, Word, ListeningExercise, ReadingPassage,
    LessonWord, LessonListening, LessonReading,
    UserProgress, UserWordKnowledge, UserListeningProgress, UserReadingProgress,
    ReviewSession, WordReview
)

# Inline admin classes for lesson content
class LessonWordInline(admin.TabularInline):
    model = LessonWord
    extra = 0
    ordering = ['order']

class LessonListeningInline(admin.TabularInline):
    model = LessonListening
    extra = 0
    ordering = ['order']

class LessonReadingInline(admin.TabularInline):
    model = LessonReading
    extra = 0
    ordering = ['order']

# Main content admin classes
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order', 'created_at']
    inlines = [LessonWordInline, LessonListeningInline, LessonReadingInline]

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['spanish_word', 'english_translation', 'created_at']
    list_filter = ['created_at']
    search_fields = ['spanish_word', 'english_translation', 'example_sentence_spanish']
    ordering = ['spanish_word']

@admin.register(ListeningExercise)
class ListeningExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_seconds', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'transcript']
    ordering = ['title']

@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display = ['title', 'word_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'content']
    ordering = ['title']

# User progress admin classes
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'score', 'completion_date']
    list_filter = ['is_completed', 'completion_date']
    search_fields = ['user__username', 'lesson__title']
    ordering = ['-last_accessed']

@admin.register(UserWordKnowledge)
class UserWordKnowledgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'word', 'knowledge_level', 'review_count', 'next_review_date']
    list_filter = ['knowledge_level', 'last_reviewed']
    search_fields = ['user__username', 'word__spanish_word', 'word__english_translation']
    ordering = ['next_review_date']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'word')

@admin.register(UserListeningProgress)
class UserListeningProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'listening_exercise', 'is_completed', 'best_score', 'times_attempted']
    list_filter = ['is_completed']
    search_fields = ['user__username', 'listening_exercise__title']
    ordering = ['-updated_at']

@admin.register(UserReadingProgress)
class UserReadingProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'reading_passage', 'is_completed', 'score', 'times_read']
    list_filter = ['is_completed']
    search_fields = ['user__username', 'reading_passage__title']
    ordering = ['-updated_at']

@admin.register(ReviewSession)
class ReviewSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'started_at', 'total_items', 'correct_answers', 'accuracy']
    list_filter = ['session_type', 'started_at']
    search_fields = ['user__username']
    ordering = ['-started_at']

@admin.register(WordReview)
class WordReviewAdmin(admin.ModelAdmin):
    list_display = ['session', 'word_knowledge', 'is_correct', 'response_time_ms', 'reviewed_at']
    list_filter = ['is_correct', 'reviewed_at']
    ordering = ['-reviewed_at']
