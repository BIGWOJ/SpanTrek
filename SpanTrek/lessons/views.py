from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Lesson, Country, Vocabulary, Sentence, Audio, Landmark
from django.db.models import Sum, Case, When, Value, IntegerField


@login_required
def world_map(request):
    # Handle POST request for continue adventure button
    if request.POST.get('action') == 'continue_adventure':
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
    # Get lesson count for this country
    country_obj = Country.objects.filter(name__iexact=country).first()
    country_lessons_count = Lesson.objects.filter(country=country_obj).count() if country_obj else 0
    user_country_progress = request.user.country_lessons_progress.get(country, 0)

    # Country learning progress
    country_lessons = Lesson.objects.filter(country=country_obj)

    country_vocabularies = Vocabulary.objects.filter(lessons__in=country_lessons).distinct()
    country_sentences = Sentence.objects.filter(lessons__in=country_lessons).distinct()
    country_audios = Audio.objects.filter(lessons__in=country_lessons).distinct()
    country_use_of_spanish = country_lessons.aggregate(total=Sum('use_of_spanish'))['total'] or 0
    
    country_stats_dict = {
        'vocabularies': country_vocabularies.count(),
        'sentences': country_sentences.count(),
        'audios': country_audios.count(),
        'use_of_spanish': country_use_of_spanish,
    }

    user_learned_words = request.user.words_learned or []
    user_country_vocabularies_count = country_vocabularies.filter(word__in=user_learned_words).count()

    user_learned_sentences = request.user.sentences_learned or []    
    user_country_sentences_count = country_sentences.filter(sentence__in=user_learned_sentences).count()

    user_learned_audio = request.user.audio_learned or []
    user_country_audio_count = country_audios.filter(text__in=user_learned_audio).count()
    
    # Get lessons ordered by landmark id and then by lesson order within landmark
    all_lessons_in_order = Lesson.objects.filter(country=country_obj).order_by('country_order', 'order')
    
    user_lessons_completed = request.user.country_lessons_progress.get(country, 0)
    user_use_of_spanish = all_lessons_in_order[:user_lessons_completed].aggregate(total=Sum('use_of_spanish'))['total'] or 0

    user_country_progress_dict = {
        'vocabularies': user_country_vocabularies_count,
        'sentences': user_country_sentences_count,
        'audios': user_country_audio_count,
        'use_of_spanish': user_use_of_spanish,
    }

    overall_percentage = round((sum(user_country_progress_dict.values()) / sum(country_stats_dict.values())) * 100 if sum(country_stats_dict.values()) > 0 else 0)

    context = {
        'progress_bar_max': country_lessons_count,
        'country': country,
        'progress_bar_progress': user_country_progress,
        'country_stats_dict': country_stats_dict,
        'user_country_progress': user_country_progress,
        'user_country_progress_dict': user_country_progress_dict,
        'overall_percentage': overall_percentage,
    }

    return render(request, f'lessons/{country}/country.html', context=context)


@login_required
def country_landmark_lesson(request, country, landmark, lesson_number=None, exercise_number=None):
    # Get the current progress for this landmark from the user's profile
    landmark_progress = request.user.landmark_lessons_progress.get(landmark, 0)
    user_landmark_progress = request.user.landmark_lessons_progress.get(landmark, 0)
    country_obj = Country.objects.filter(name__iexact=country).first()
    landmark_obj = Landmark.objects.filter(name__iexact=landmark).first()
    
    # If lesson_number is not provided, show intro page first
    if lesson_number is None:
        # Get all lessons for this landmark
        landmark_lessons = Lesson.objects.filter(landmark=landmark_obj, country=country_obj).order_by('order')

        context = {
            'landmark': landmark,
            'country': country,
            'landmark_lessons': landmark_lessons,
            'user_landmark_progress': user_landmark_progress,
        }
        return render(request, 'lessons/lesson_intro.html', context)

    # Get the lesson
    current_lesson = lesson_number
    lesson = Lesson.objects.filter(landmark=landmark_obj, order=current_lesson).first()
    
    if not lesson:
        # Handle case where lesson doesn't exist
        context = {
            'landmark': landmark,
            'country': country,
        }
        return render(request, 'lessons/lesson_base.html', context=context)
    
    # Get lesson sequence items
    lesson_sequence_items = lesson.lesson_sequence or []
    
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
    
    exercise_item = lesson_sequence_items[current_exercise_index]
    current_block = exercise_item.get('type')
    current_content = exercise_item.get('content')

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
    # Get the country and landmark objects
    country_obj = Country.objects.filter(name__iexact=country).first()
    if not country_obj:
        return redirect('lessons:world_map')
    
    from .models import Landmark
    landmark_obj = Landmark.objects.filter(name__iexact=landmark, country=country_obj).first()
    if not landmark_obj:
        return redirect('lessons:country_map', country=country)
    
    # Get the completed lesson
    lesson = Lesson.objects.filter(landmark=landmark_obj, order=lesson_number).first()

    # If lesson doesn't exist, redirect back to landmark map
    if not lesson:
        return redirect('lessons:country_landmark_lesson', country=country, landmark=landmark)
    
    # Check if there's a next lesson
    next_lesson = Lesson.objects.filter(landmark=landmark_obj, order=lesson_number + 1).first()

    lesson_completed_before = request.user.landmark_lessons_progress.get(landmark, 0) >= lesson_number+1
    print(request.user.landmark_lessons_progress.get(landmark, 0), lesson_number+1)
    request.user.update_progress_after_lesson(landmark, lesson_number, lesson_completed_before)
    
    # Calculate total exercises
    total_exercises = len(lesson.lesson_sequence)
    
    context = {
        'landmark': landmark,
        'country': country,
        'lesson': lesson,
        'lesson_number': lesson_number,
        'next_lesson_number': lesson_number + 1 if next_lesson else None,
        'has_next_lesson': next_lesson is not None,
        'total_exercises': total_exercises,
        'lesson_completed_before': lesson_completed_before,
    }

    country_lessons = Lesson.objects.filter(country__name__iexact=country).count()  

    # Country completed
    if request.user.country_lessons_progress.get(country, 0) >= country_lessons and not lesson_completed_before:
        return country_complete(request, country)

    return render(request, 'lessons/lesson_complete.html', context=context)


@login_required
def country_complete(request, country):
    """View for country completion page with congratulations and statistics"""  
    country_obj = Country.objects.filter(name__iexact=country).first()
    country_lessons = Lesson.objects.filter(country=country_obj).count()
    country_knowledge = {
        'vocabularies': Vocabulary.objects.filter(lessons__country=country_obj).distinct().count(),
        'sentences': Sentence.objects.filter(lessons__country=country_obj).distinct().count(),
        'audios': Audio.objects.filter(lessons__country=country_obj).distinct().count(),
        'use_of_spanish': Lesson.objects.filter(country=country_obj).aggregate(total=Sum('use_of_spanish'))['total'] or 0,
    }
    
    if country not in request.user.passports_earned:
        request.user.passports_earned.append(country)
        request.user.save()

    context = {
        'country': country,
        'total_lessons': country_lessons,
        'country_knowledge': country_knowledge,
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

@login_required
def continue_adventure_button(request):
    pass