from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def world_map(request):
   
    return render(request, 'lessons/world_map.html')


@login_required
def spain_view(request):
    
    return render(request, 'lessons/spain.html')

@login_required
def peru_view(request):

    return render(request, 'lessons/peru.html')


@login_required
def mexico_view(request):

    return render(request, 'lessons/mexico.html')
    
