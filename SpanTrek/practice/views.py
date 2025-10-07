from django.shortcuts import render


def random_practice(request):
    return render(request, 'practice/random_practice.html')