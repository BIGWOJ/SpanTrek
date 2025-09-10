from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def world_map(request):
    return render(request, 'lessons/world_map.html')


@login_required
def country_view(request, country):
    template_name = f'lessons/{country}/country.html'
    return render(request, template_name)

@login_required
def lesson_view(request, country, lesson):
    template_name = f'lessons/{country}/{lesson}.html'
    return render(request, template_name)

@login_required
def city_lesson_view(request, city, lesson_number):
    context = {
        'city': city,
        'lesson_number': lesson_number,
        'prev_lesson': lesson_number - 1 if lesson_number > 1 else None,
        'next_lesson': lesson_number + 1 if lesson_number < 4 else None,
    }
    template_name = f'lessons/poland/{city}/lesson_{lesson_number}.html'
    return render(request, template_name, context)