from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from .models import User
from lessons.models import Lesson, Vocabulary, Sentence
from .forms import My_User_Creation_Form
from .services import AchievementService
import os
from datetime import date
from django.contrib.auth.decorators import login_required


@login_required
def home_page(request):
    # If user is not authenticated, redirect to login page
    if not request.user.is_authenticated:
        return redirect('login_page')
    request.user.progress_daily_challenges()
    # Create a new daily challenge for the user
    if request.user.daily_challenges_creation_date is None or request.user.daily_challenges_creation_date < date.today():
        request.user.daily_challenges_creation_date = date.today()
        request.user.create_daily_challenges()
        request.user.save()

    all_lessons_count = Lesson.objects.count()
    completed_daily_challenges_count = sum(1 for challenge in request.user.daily_challenges if challenge['completed'])
    daily_challenges = request.user.daily_challenges

    context = {
        'all_lessons_count': all_lessons_count,
        'completed_daily_challenges_count': completed_daily_challenges_count,
        'daily_challenges': daily_challenges,
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

@login_required
def user_page(request, pk):
    user = User.objects.get(id=pk)
    
    # Update settings 
    if request.method == 'POST':
        # Avatar upload
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            
            # Validate file type despite in HTML accept attribute (can be bypassed)
            valid_types = ['image/jpg', 'image/jpeg', 'image/png']

            if avatar_file.content_type not in valid_types:
                messages.error(request, 'Please select a valid image file (JPG, PNG)')
                return redirect('user_page', pk=user.id)
            
            # Validate file size up to 5MB
            max_size = 5 * 1024 * 1024
            if avatar_file.size > max_size:
                messages.error(request, 'File size must be less than 5MB')
                return redirect('user_page', pk=user.id)
                        
            # If all validations passed, save the file
            user.avatar = avatar_file
            user.save()
            messages.success(request, 'Profile picture updated successfully')
        
        if request.POST.get('email') and request.POST['email'] != user.email:
            user.email = request.POST['email']
            user.save()
            messages.success(request, 'Email updated successfully')

        if request.POST.get('current_password') and request.POST['current_password'] != '':
            if user.check_password(request.POST['current_password']):
                new_password = request.POST.get('new_password', '')
                confirm_password = request.POST.get('confirm_password', '')
                if new_password == '' or confirm_password == '':
                    messages.error(request, 'New password fields cannot be empty')
                    return redirect('user_page', pk=user.id)
                if new_password == confirm_password:
                    if user.check_password(new_password) or user.check_password(confirm_password):
                        messages.error(request, 'New password cannot be the same as the current password')
                        return redirect('user_page', pk=user.id)
                    user.set_password(new_password)
                    login(request, user)  
                    user.save()
                    messages.success(request, 'Password updated successfully')
                else:
                    messages.error(request, 'New password and confirmation do not match')
            else:
                messages.error(request, 'Current password is incorrect')
            

    # Experience calculations
    xp_for_next_level = (user.level * 500) - user.experience
    progress_percentage = min(100, (user.experience / xp_for_next_level) * 100) if xp_for_next_level > 0 else 0

    user_level_name = get_user_level_name(user.level)
    
    # Achievements
    achievements = AchievementService.get_user_achievements_status_exp(user)

    achievements_earned_count = sum(1 for ach in achievements if ach['earned'])
    total_achievements_count = len(achievements)
    achievement_earned_percentage = (achievements_earned_count / total_achievements_count * 100) if total_achievements_count > 0 else 0
    
    words_learned_count = len(user.words_learned)
    total_words_count = Vocabulary.objects.count()
    words_learned_percentage = (words_learned_count / total_words_count * 100) if total_words_count > 0 else 0

    total_sentences_count = Sentence.objects.count()
    sentences_learned_count = len(user.sentences_learned)
    sentences_learned_percentage = (sentences_learned_count / total_sentences_count * 100) if total_sentences_count > 0 else 0

    total_use_of_spanish = Lesson.objects.aggregate(total=models.Sum('use_of_spanish'))['total'] or 0
    use_of_spanish_percentage = (user.use_of_spanish / total_use_of_spanish * 100) if total_use_of_spanish > 0 else 0

    total_lessons_count = Lesson.objects.count()
    lessons_completed_percentage = (user.adventure_progress / total_lessons_count * 100) if total_lessons_count > 0 else 0

    
    context = {
        'user': user,
        
        'xp_for_next_level': xp_for_next_level,
        'progress_percentage': progress_percentage,
        'user_level_name': user_level_name,

        'completed_lessons': user.adventure_progress,
        'total_lessons': total_lessons_count,
        'lessons_completed_percentage': lessons_completed_percentage,

        'achievements': achievements,
        'total_achievements': total_achievements_count,
        'achievement_earned_percentage': achievement_earned_percentage,

        'words_learned_count': words_learned_count,
        'total_words_count': total_words_count,
        'words_learned_percentage': words_learned_percentage,

        'sentences_learned_count': sentences_learned_count,
        'total_sentences_count': total_sentences_count,
        'sentences_learned_percentage': sentences_learned_percentage,

        'spanish_usage_count': user.use_of_spanish,
        'total_usage_count': total_use_of_spanish,
        'spanish_usage_percentage': use_of_spanish_percentage,
        
        'user_activity_days': user.activity_days,
    }

    return render(request, 'base/user_page.html', context)

@login_required
def leaderboard_page(request, view_type):
    all_users_count = User.objects.all().count()
    
    top_10_users = []
    leaderboard_users = []
    country_leaders = []
    
    if view_type == 'top':
        leaderboard_users = User.objects.all().order_by('-experience')[:10]
        for i, user in enumerate(leaderboard_users):
            user.display_rank = i + 1
            
    elif view_type == 'user_position':
        # Get surrounding users (5 below + current user + 5 above)
        users_below = User.objects.filter(experience__lt=request.user.experience).order_by('-experience')[:5]
        users_above = User.objects.filter(experience__gt=request.user.experience).order_by('experience')[:5]
        users_same_exp = User.objects.filter(experience=request.user.experience).exclude(id=request.user.id).order_by('id')
        
        # Combine and order properly
        leaderboard_users = list(users_below)[::-1] + list(users_same_exp) + [request.user] + list(users_above)
        leaderboard_users.reverse()
        
        # Calculate starting rank for the first user in the list
        if leaderboard_users:
            first_user = leaderboard_users[0]
            start_rank = User.objects.filter(experience__gt=first_user.experience).count() + 1
            
            # Assign ranks
            for i, user in enumerate(leaderboard_users):
                user.display_rank = start_rank + i

    context = {
        'all_users_count': all_users_count,
        'top_10_users': top_10_users,
        'leaderboard_users': leaderboard_users,
        'country_leaders': country_leaders,
        'view_type': view_type,
    }
    return render(request, 'base/leaderboard.html', context)

def get_user_level_name(level):
    if level >= 25:
        return "El Campeón"
    elif level >= 20:
        return "Expert Explorer"
    elif level >= 15:
        return "Advanced Explorer"
    elif level >= 10:
        return "Intermediate Explorer"
    elif level >= 5:
        return "Dedicated Learner"
    else:
        return "Beginner Explorer"
    
