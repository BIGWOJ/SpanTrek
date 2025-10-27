from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Lesson, Country



@login_required
def world_map(request):
    # Handle POST request for continue adventure button
    if request.method == 'POST' and request.POST.get('action') == 'continue_adventure':
        continue_adventure_button(request)
    
    progress_bar_progress = request.user.country_lessons_progress
    user_progress = sum(progress_bar_progress.values())
    user_countries_progress = request.user.country_lessons_progress
    all_lessons_count = Lesson.objects.count()

    all_countries = Country.objects.all()
    countries_lessons_dict = {}
    for country_obj in all_countries:
        countries_lessons_dict[country_obj.name] = Lesson.objects.filter(country=country_obj).count()

    # Calculate completion status for each country
    country_completion_status = {}
    for country_name, total_lessons in countries_lessons_dict.items():
        completed = user_countries_progress.get(country_name, 0)
        country_completion_status[country_name] = (completed == total_lessons and total_lessons > 0)
        
    context = {
        'progress_bar_progress': user_progress,
        'progress_bar_max': all_lessons_count,
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
        'progress_bar_max': country_lessons_count,
        'country': country,
        'progress_bar_progress': user_country_progress,
    }

    return render(request, template_name, context)


@login_required
def country_landmark_lesson(request, country, landmark, lesson_number=None, exercise_number=None):
    # Get the current progress for this landmark from the user's profile
    landmark_progress = request.user.landmark_lessons_progress.get(landmark, 0)
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

    # Get the lesson
    current_lesson = lesson_number
    lesson = Lesson.objects.filter(landmark=landmark, order=current_lesson).first()
    
    if not lesson:
        # Handle case where lesson doesn't exist
        context = {
            'landmark': landmark,
            'country': country,
            'error': 'Lesson not found'
        }
        return render(request, 'lessons/lesson_base.html', context=context)
    
    # Get lesson sequence items as a list of tuples
    lesson_sequence_items = list(lesson.lesson_sequence.items()) if lesson.lesson_sequence else []
    total_exercises = len(lesson_sequence_items)
    
    # If exercise_number is not provided, redirect to first exercise
    if exercise_number is None and lesson_sequence_items:
        return redirect('lessons:landmark_lesson_with_exercise', 
                       country=country, landmark=landmark, 
                       lesson_number=lesson_number, exercise_number=1)
    
    # If no exercises in lesson, show lesson overview
    if not lesson_sequence_items:
        context = {
            'landmark': landmark,
            'country': country,
            'lesson': lesson,
            'lesson_vocabularies': lesson.vocabularies.all(),
            'lesson_sentences': lesson.sentences.all(),
            'lesson_number': current_lesson,
            'prev_lesson_number': current_lesson - 1 if current_lesson >= 1 else None,
            'next_lesson_number': current_lesson + 1 if current_lesson < 3 else None,
            'error': 'No exercises found in this lesson'
        }
        return render(request, 'lessons/lesson_base.html', context=context)
    
    # Validate exercise_number
    if exercise_number < 1 or exercise_number > total_exercises:
        return redirect('lessons:landmark_lesson_with_exercise', 
                       country=country, landmark=landmark, 
                       lesson_number=lesson_number, exercise_number=1)
    
    # Get current exercise (convert to 0-based index)
    current_exercise_index = exercise_number - 1
    current_block, current_content = lesson_sequence_items[current_exercise_index]

    context = {
        'landmark': landmark,
        'country': country,
        'lesson': lesson,
        'lesson_vocabularies': lesson.vocabularies.all(),
        'lesson_sentences': lesson.sentences.all(),
        'lesson_number': current_lesson,
        'exercise_number': exercise_number-1,
        'exercise_done': False,
        'total_exercises': total_exercises,
        'current_block': current_block,
        'current_content': current_content,
        'prev_lesson_number': current_lesson - 1 if current_lesson >= 1 else None,
        'next_lesson_number': current_lesson + 1 if current_lesson < 3 else None,
        'prev_exercise_number': exercise_number - 1 if exercise_number > 1 else None,
        'next_exercise_number': exercise_number + 1 if exercise_number < total_exercises else None,
        'is_last_exercise': exercise_number == total_exercises,
        'is_first_exercise': exercise_number == 1,
    }

    return render(request, 'lessons/lesson_base.html', context=context)


@login_required
def lesson_complete(request, country, landmark, lesson_number):
    """View for lesson completion page with congratulations message"""
    # Get the completed lesson
    lesson = Lesson.objects.filter(landmark=landmark, order=lesson_number).first()

    if not lesson:
        # If lesson doesn't exist, redirect back to landmark
        return redirect('lessons:country_landmark_lesson', country=country, landmark=landmark)
    
    # Check if there's a next lesson
    next_lesson = Lesson.objects.filter(landmark=landmark, order=lesson_number + 1).first()
    
    request.user.update_progress_after_lesson(landmark, lesson_number)
    
    context = {
        'landmark': landmark,
        'country': country,
        'lesson': lesson,
        'lesson_number': lesson_number,
        'next_lesson_number': lesson_number + 1 if next_lesson else None,
        'has_next_lesson': next_lesson is not None,
        'total_exercises': len(list(lesson.lesson_sequence.items())) if lesson.lesson_sequence else 0,
    }

    country_lessons = Lesson.objects.filter(country__name__iexact=country).count()    
    # Country completed
    if request.user.country_lessons_progress.get(country, 0) >= country_lessons:
        return country_complete(request, country)

    return render(request, 'lessons/lesson_complete.html', context=context)


@login_required
def country_complete(request, country):
    """View for country completion page with congratulations and statistics"""  
    country_obj = Country.objects.filter(name__iexact=country).first()
    country_lessons = Lesson.objects.filter(country=country_obj).count()
    xp_gained = country_lessons * 50
    
    context = {
        'country': country,
        'total_lessons': country_lessons,
        'xp_gained': xp_gained,
    }
    
    
    return render(request, 'lessons/country_complete.html', context=context)


@login_required
def check_exercise_done(request):
    """Handle exercise completion - supports both AJAX and regular form submission"""
    if request.method == 'POST':
        # Get all answer fields
        answers = {}
        
        for key, value in request.POST.items():
            if key.startswith('answer_'):
                answers[key] = value.strip()
        
        # Get additional data
        exercise_completed = request.POST.get('exercise_completed', 'false').lower() == 'true'
 
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response for AJAX
            response_data = {
                'success': True,
                'message': 'Exercise completed successfully',
                'exercise_completed': exercise_completed,
                'answers_received': len(answers),
            }
            return JsonResponse(response_data)
        else:
            # Handle regular form submission (redirect or render)
            # You might want to redirect to next exercise or show results
            return redirect('lessons:world_map')  # or wherever you want to redirect

    # Handle GET request
    return JsonResponse({'error': 'Method not allowed'}, status=405)

