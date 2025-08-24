from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Country, AdventureLesson


@login_required
def world_map(request):
    """
    World map page - displays interactive map with Spanish-speaking countries
    """
    # Get all Spanish-speaking countries
    countries = Country.objects.all()
    
    # Calculate statistics for each country
    country_stats = {}
    for country in countries:
        country_key = country.name.lower().replace(' ', '_')
        total_lessons = AdventureLesson.objects.filter(country=country).count()
        completed_lessons = AdventureLesson.objects.filter(
            country=country,
            userlesson__user=request.user,
            userlesson__completed=True
        ).distinct().count()
        
        country_stats[country_key] = {
            'completed': completed_lessons,
            'total': total_lessons
        }
    context = {
        'page_title': 'World Map - Spanish Speaking Countries',
        'country_stats': country_stats
    }

    context = {
        'page_title': 'World Map - Spanish Speaking Countries',
        'country_stats': country_stats
    }
    return render(request, 'lessons/world_map.html', context)

