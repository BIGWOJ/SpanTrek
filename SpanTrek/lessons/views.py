from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lesson

from .models import Country


@login_required
def world_map(request):
    return render(request, 'lessons/world_map.html')


@login_required
def country_view(request, country):
    template_name = f'lessons/{country}/country.html'
    # Get lesson count for this country
    country_obj = Country.objects.filter(name__iexact=country).first()
    country_lessons_count = Lesson.objects.filter(country=country_obj).count() if country_obj else 0
    user_country_progress = request.user.country_lessons_progress.get(country, 0)
    
    context = {
        'country_lessons_count': country_lessons_count,
        'country': country,
        'user_country_progress': user_country_progress,
    }
    return render(request, template_name, context)


@login_required
def country_landmark_lesson(request, country, landmark, lesson_number=None):
    # Get the current progress for this landmark from the user's profile
    landmark_progress = request.user.landmark_lessons_progress.get(landmark, 1)

    user_landmark_progress = request.user.landmark_lessons_progress.get(landmark, 0)
    
    # If lesson_number is not provided, show intro page first
    if lesson_number is None:
        lesson = Lesson.objects.filter(landmark=landmark, order=landmark_progress).first()
        context = {
            'landmark': landmark,
            'country': country,
            'lesson': lesson,
            'start_lesson_url': f"/{country}/{landmark}/{landmark_progress}/",
            'user_landmark_progress': user_landmark_progress,
        }

        return render(request, 'lessons/lesson_intro.html', context)

    # Otherwise, show the actual lesson page
    current_lesson = lesson_number
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

    return render(request, 'lessons/lesson_base.html', context)


