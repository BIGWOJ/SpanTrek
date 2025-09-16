from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lesson


@login_required
def world_map(request):
    return render(request, 'lessons/world_map.html')


@login_required
def country_view(request, country):
    template_name = f'lessons/{country}/country.html'
    return render(request, template_name)


@login_required
def country_landmark_lesson(request, country, landmark, lesson_number=None):
    # Get the current progress for this landmark from the user's profile
    landmark_progress = request.user.landmark_lessons_progress.get(landmark, 1)
    
    # If lesson_number is not provided, use the current progress
    current_lesson = lesson_number if lesson_number is not None else landmark_progress

    lesson = Lesson.objects.filter(landmark=landmark, order=current_lesson).first()

    context = {
        'landmark': landmark,
        'country': country,
        'lesson': lesson,
        'lesson_vocabularies': lesson.vocabularies.all() if lesson else [],
        'lesson_sentences': lesson.sentences.all() if lesson else [],
        'lesson_number': current_lesson,
        'prev_lesson_number': current_lesson - 1 if current_lesson >= 1 else None,
        'next_lesson_number': current_lesson + 1 if current_lesson < 3 else None,
    }

    template_name = f'lessons/{country}/{landmark}/lesson_{current_lesson}.html'

    return render(request, 'lessons/lesson_base.html', context)

