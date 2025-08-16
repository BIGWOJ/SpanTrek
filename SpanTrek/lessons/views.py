from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def world_map(request):
    """
    World map page - displays interactive map with Spanish-speaking countries
    """
    context = {
        'page_title': 'World Map - Spanish Speaking Countries'
    }
    return render(request, 'lessons/world_map.html', context)

