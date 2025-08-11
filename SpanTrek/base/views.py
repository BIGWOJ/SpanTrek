from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Achievement, UserAchievement
from .forms import My_User_Creation_Form

def home_page(request):
    # If user is not authenticated, redirect to login page
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    return render(request, 'home.html')


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
    return render(request, 'login_register.html', context)

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
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login_page')

def user_page(request, pk):
    user = User.objects.get(id=pk)
    
    # Check and award any new achievements
    newly_awarded = user.check_and_award_achievements()
    
    # Show message for newly awarded achievements
    if newly_awarded:
        for achievement in newly_awarded:
            messages.success(request, f'🎉 Achievement Unlocked: {achievement.name}!')
            # Award XP bonus
            user.experience += achievement.points_reward
        user.save()
    
    # Calculate some additional stats for the user page
    xp_for_next_level = ((user.level) * 100) + 200  # Example formula
    xp_needed = max(0, xp_for_next_level - user.experience)
    progress_percentage = min(100, (user.experience / xp_for_next_level) * 100) if xp_for_next_level > 0 else 0
    
    # Get user's achievements from database
    user_achievements = user.get_user_achievements()
    earned_achievement_ids = set(ua.achievement.id for ua in user_achievements)
    
    # Get all achievements for display (earned and unearned)
    all_achievements = Achievement.objects.filter(is_active=True).order_by('condition_value')
    
    achievements_data = []
    for achievement in all_achievements:
        # Skip hidden achievements that haven't been earned
        if achievement.is_hidden and achievement.id not in earned_achievement_ids:
            continue
            
        earned_date = None
        if achievement.id in earned_achievement_ids:
            user_achievement = next(ua for ua in user_achievements if ua.achievement.id == achievement.id)
            earned_date = user_achievement.earned_at
        
        achievements_data.append({
            'id': achievement.id,
            'name': achievement.name,
            'description': achievement.description,
            'icon': achievement.icon,
            'earned': achievement.id in earned_achievement_ids,
            'earned_date': earned_date,
            'condition_type': achievement.condition_type,
            'condition_value': achievement.condition_value,
            'points_reward': achievement.points_reward,
            'progress': get_achievement_progress(user, achievement),
        })
    
    # Calculate achievement stats
    total_achievements = len(achievements_data)
    earned_count = len(earned_achievement_ids)
    achievement_percentage = (earned_count / total_achievements * 100) if total_achievements > 0 else 0
    
    context = {
        'user': user,
        'xp_needed': xp_needed,
        'progress_percentage': progress_percentage,
        'achievements': achievements_data,
        'total_achievements': total_achievements,
        'earned_achievements': earned_count,
        'achievement_percentage': achievement_percentage,
        'newly_awarded': newly_awarded,
    }
    
    return render(request, 'user_page.html', context)

def get_achievement_progress(user, achievement):
    """Calculate progress towards an achievement (0-100%)"""
    if achievement.condition_type == 'experience':
        current = user.experience
    elif achievement.condition_type == 'level':
        current = user.level
    elif achievement.condition_type == 'streak':
        current = user.days_streak
    elif achievement.condition_type == 'adventure_progress':
        current = user.adventure_progress
    else:
        # For custom achievements, return 0 or 100
        return 100 if achievement.check_condition(user) else 0
    
    target = achievement.condition_value
    progress = min(100, (current / target * 100)) if target > 0 else 0
    return round(progress, 1)