from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lesson, Country


@login_required
def world_map(request):
    user_country_progress = request.user.country_lessons_progress
    user_progress = sum(user_country_progress.values())
    user_countries_progress = request.user.country_lessons_progress
    all_lessons_count = Lesson.objects.count()

    all_countries = Country.objects.all()
    countries_lessons_dict = {}
    for country_obj in all_countries:
        countries_lessons_dict[country_obj.name] = Lesson.objects.filter(country=country_obj).count()

    # country_color_class = "lessons_done" if user_countries_progress.get(country_obj.name, 0) > 0 else "spanish-country"

    # Calculate completion status for each country
    country_completion_status = {}
    for country_name, total_lessons in countries_lessons_dict.items():
        completed = user_countries_progress.get(country_name, 0)
        country_completion_status[country_name] = (completed == total_lessons and total_lessons > 0)
    print(country_completion_status)
    context = {
        'user_progress': user_progress,
        'all_lessons_count': all_lessons_count,
        'user_countries_progress': user_countries_progress,
        'countries_lessons_dict': countries_lessons_dict,
        'country_completion_status': country_completion_status,
    }
    return render(request, "lessons/world_map.html", context=context)


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


