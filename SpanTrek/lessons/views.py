from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lesson

from .models import Country


@login_required
def world_map(request):
    # Example locations for Poland
    locations = [
        {"name": "Szczecin", "lat": "53.4285", "lng": "14.5528", "id": 1, "url": "/lessons/poland/szczecin/"},
        {"name": "Krakow", "lat": "50.0647", "lng": "19.9450", "id": 2, "url": "/lessons/poland/krakow/"},
        {"name": "Gdansk", "lat": "54.3520", "lng": "18.6466", "id": 3, "url": "/lessons/poland/gdansk/"},
        {"name": "Poznan", "lat": "52.4064", "lng": "16.9252", "id": 4, "url": "/lessons/poland/poznan/"},
        {"name": "Warsaw", "lat": "52.2297", "lng": "21.0122", "id": 5, "url": "/lessons/poland/warsaw/"},
    ]
    user_progress = request.user.landmark_lessons_progress if hasattr(request.user, 'landmark_lessons_progress') else {}
    for loc in locations:
        progress = user_progress.get(loc["name"].lower(), 0)
        if progress >= 3:
            loc["image_url"] = f"/static/images/map_pins/pin{loc['id']}_done.svg"
        else:
            loc["image_url"] = f"/static/images/map_pins/pin{loc['id']}.svg"
    context = {"locations": locations}
    return render(request, "lessons/world_map.html", context)


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


