from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from lessons.models import Lesson
from .forms import My_User_Creation_Form
from .services import AchievementService

def home_page(request):
    # If user is not authenticated, redirect to login page
    if not request.user.is_authenticated:
        return redirect('login_page')
    

    all_lessons_count = Lesson.objects.count()

    context = {
        'all_lessons_count': all_lessons_count,
    }
    return render(request, 'base/home.html', context)

def login_page(request):
    page = 'login'
    # If user is already logged in, redirect to home page from login page
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        error_message = False
        print(email, password)
        
        try:
            user = User.objects.get(email=email)
        except:
            error_message = True
            messages.error(request, 'Password or email is incorrect')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            if not error_message:
                messages.error(request, 'Password or email is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def register_page(request):
    page = 'register'
    form = My_User_Creation_Form()
        
    if request.method == 'POST':
        form = My_User_Creation_Form(request.POST)
        if form.is_valid():
            # Commit=false -> not saving to database yet, firstly clearing up data and logging up on the page
            user = form.save(commit=False)
            # user.username = user.username
            user.save()
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Coś poszło nie tak. Spróbuj ponownie')

    context = {'register_form': form, 'page': page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login_page')

def user_page(request, pk):
    user = User.objects.get(id=pk)
    
    # Calculate some additional stats for the user page
    xp_for_next_level = ((user.level) * 100) + 200  # Example formula
    xp_needed_next_lvl = max(0, xp_for_next_level - user.experience)
    progress_percentage = min(100, (user.experience / xp_for_next_level) * 100) if xp_for_next_level > 0 else 0
    
    # Get achievements with earned status
    achievements = AchievementService.get_user_achievements_with_status(user)
    
    # Count earned achievements
    earned_count = sum(1 for ach in achievements if ach['earned'])
    
    context = {
        'user': user,
        'xp_needed_next_lvl': xp_needed_next_lvl,
        'progress_percentage': progress_percentage,
        'achievements': achievements,
        'earned_count': earned_count,
    }
    print('aaa')
    return render(request, 'base/user_page.html', context)
