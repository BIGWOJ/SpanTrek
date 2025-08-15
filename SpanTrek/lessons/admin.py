from django.contrib import admin
from .models import Country, AdventureLesson, AdventureLessonContent, Exercise, UserLessonProgress, Vocabulary

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(AdventureLesson)  
class AdventureLessonAdmin(admin.ModelAdmin):
    list_display = ['lesson_id', 'country', 'order', 'experience_points', 'required_score']
    list_filter = ['country']
    ordering = ['country', 'order']

@admin.register(AdventureLessonContent)
class AdventureLessonContentAdmin(admin.ModelAdmin):
    list_display = ['content_id', 'lesson', 'content_type', 'title', 'order']
    list_filter = ['content_type', 'lesson']
    ordering = ['lesson', 'order']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'exercise_type', 'order', 'points']
    list_filter = ['exercise_type', 'lesson']
    ordering = ['lesson', 'order']

@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_started', 'is_completed', 'score', 'max_score']
    list_filter = ['is_started', 'is_completed']
    search_fields = ['user__username']

@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation', 'pronunciation']
    search_fields = ['word', 'translation']
