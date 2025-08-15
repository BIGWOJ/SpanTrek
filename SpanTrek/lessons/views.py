from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lesson


@login_required
def lessons_home(request):
    """
    Strona główna lekcji - lista dostępnych lekcji do wyboru
    """
    # Pobierz wszystkie aktywne lekcje
    lessons = Lesson.objects.filter(is_active=True)
    
    # Tymczasowo bez tabeli progress - będzie dodana po migracji
    lessons_with_progress = []
    for lesson in lessons:
        lesson_data = {
            'lesson': lesson,
            'progress': None,
            'is_completed': False,
            'score': 0
        }
        lessons_with_progress.append(lesson_data)
    
    context = {
        'lessons_with_progress': lessons_with_progress,
        'total_lessons': lessons.count(),
        'completed_lessons': 0  # Tymczasowo 0 
    }
    
    return render(request, 'lessons/lessons_home.html', context)
