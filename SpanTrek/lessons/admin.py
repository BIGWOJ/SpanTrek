from django.contrib import admin
from .models import *

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']
    search_fields = ['name']

    
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'landmark', 'country']
    list_filter = ['landmark', 'country']
    search_fields = ['title', 'content']
    ordering = ['landmark', 'order']


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation']
    search_fields = ['word', 'translation']
    

@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ['sentence', 'translation']
    search_fields = ['sentence', 'translation']

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['text', 'audio_url']
    search_fields = ['text']