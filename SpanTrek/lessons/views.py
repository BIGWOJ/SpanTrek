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
def country_city_lesson(request, country, city, lesson_number=None):
    # Get the current progress for this city from the user's profile
    city_progress = request.user.city_lessons_progress.get(city, 1)
    
    # If lesson_number is not provided, use the current progress
    current_lesson = lesson_number if lesson_number is not None else city_progress

    lesson = Lesson.objects.filter(city=city, order=current_lesson).first()

    context = {
        'city': city,
        'country': country,
        'lesson': lesson,
        'lesson_vocabularies': lesson.vocabularies.all(),
        'lesson_sentences': lesson.sentences.all(),
        'lesson_number': current_lesson,
        'prev_lesson_number': current_lesson - 1 if current_lesson >= 1 else None,
        'next_lesson_number': current_lesson + 1 if current_lesson < 3 else None,
    }

    template_name = f'lessons/{country}/{city}/lesson_{current_lesson}.html'

    return render(request, 'lessons/lesson_base.html', context)

