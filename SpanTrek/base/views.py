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


def home_page(request):
    # If user is not authenticated, redirect to login page
    if not request.user.is_authenticated:
        return redirect('login_page')

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
    
    # Update settings 
    if request.method == 'POST':
        # Avatar upload
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            
            # Validate file type despite in HTML accept attribute (can be bypassed)
            valid_types = ['image/jpg', 'image/jpeg', 'image/png']
            print(avatar_file.content_type)
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
            print(request.POST['email'])
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
            

    # Calculate some additional stats for the user page
    xp_for_next_level = ((user.level) * 100) + 200  # Example formula
    xp_needed_next_lvl = max(0, xp_for_next_level - user.experience)
    progress_percentage = min(100, (user.experience / xp_for_next_level) * 100) if xp_for_next_level > 0 else 0
    
    # Get achievements with earned status
    achievements = AchievementService.get_user_achievements_with_status(user)

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
        
        'xp_needed_next_lvl': xp_needed_next_lvl,
        'progress_percentage': progress_percentage,

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
