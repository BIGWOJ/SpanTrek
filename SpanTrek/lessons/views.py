from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import (
    Lesson, UserProgress, UserWordKnowledge, ReviewSession
)
from .services import (
    LessonProgressService, WordKnowledgeService, ReviewSessionService,
    ContentRecommendationService
)

@login_required
def lesson_list(request):
    """Display list of available lessons"""
    lessons = Lesson.objects.filter(is_active=True).order_by('order')
    
    # Get user's progress for each lesson
    user_progress = UserProgress.objects.filter(user=request.user).select_related('lesson')
    progress_dict = {p.lesson_id: p for p in user_progress}
    
    # Add progress info to lessons
    for lesson in lessons:
        lesson.user_progress = progress_dict.get(lesson.id)
    
    # Get recommendation
    recommended_lesson = ContentRecommendationService.get_next_lesson_recommendation(request.user)
    
    context = {
        'lessons': lessons,
        'recommended_lesson': recommended_lesson,
    }
    return render(request, 'lessons/lesson_list.html', context)

@login_required
def lesson_detail(request, lesson_id):
    """Display detailed view of a lesson"""
    lesson = get_object_or_404(Lesson, id=lesson_id, is_active=True)
    
    # Get or create user progress
    progress = LessonProgressService.start_lesson(request.user, lesson)
    
    # Get lesson content
    words = lesson.lesson_words.select_related('word').order_by('order')
    listenings = lesson.lesson_listenings.select_related('listening_exercise').order_by('order')
    readings = lesson.lesson_readings.select_related('reading_passage').order_by('order')
    
    context = {
        'lesson': lesson,
        'progress': progress,
        'words': words,
        'listenings': listenings,
        'readings': readings,
    }
    return render(request, 'lessons/lesson_detail.html', context)

@login_required
@require_POST
def start_lesson(request, lesson_id):
    """Start or continue a lesson"""
    lesson = get_object_or_404(Lesson, id=lesson_id, is_active=True)
    progress = LessonProgressService.start_lesson(request.user, lesson)
    
    messages.success(request, f"Started lesson: {lesson.title}")
    return redirect('lessons:lesson_detail', lesson_id=lesson.id)

@login_required
def review_dashboard(request):
    """Dashboard showing review status and options"""
    # Check if user should review
    should_review, due_count = ContentRecommendationService.should_review(request.user)
    
    # Get vocabulary stats
    vocab_stats = WordKnowledgeService.get_user_vocabulary_stats(request.user)
    
    context = {
        'should_review': should_review,
        'due_count': due_count,
        'vocab_stats': vocab_stats,
    }
    return render(request, 'lessons/review_dashboard.html', context)

@login_required
def word_review_session(request):
    """Word review session"""
    if request.method == 'POST':
        # Start new review session
        session = ReviewSessionService.start_review_session(request.user, 'vocabulary')
        words_for_review = WordKnowledgeService.get_words_for_review(request.user)
        
        if not words_for_review:
            messages.info(request, "No words due for review right now!")
            return redirect('lessons:review_dashboard')
        
        request.session['review_session_id'] = session.id
        request.session['review_words'] = [w.id for w in words_for_review]
        request.session['current_word_index'] = 0
        
        return redirect('lessons:word_review')
    
    # Continue existing session or show current word
    session_id = request.session.get('review_session_id')
    if not session_id:
        return redirect('lessons:review_dashboard')
    
    session = get_object_or_404(ReviewSession, id=session_id, user=request.user)
    word_ids = request.session.get('review_words', [])
    current_index = request.session.get('current_word_index', 0)
    
    if current_index >= len(word_ids):
        # Session complete
        ReviewSessionService.complete_review_session(session)
        messages.success(request, f"Review complete! Accuracy: {session.accuracy:.1f}%")
        return redirect('lessons:review_dashboard')
    
    current_word_knowledge = get_object_or_404(
        UserWordKnowledge, 
        id=word_ids[current_index]
    )
    
    context = {
        'session': session,
        'word_knowledge': current_word_knowledge,
        'current_index': current_index + 1,
        'total_words': len(word_ids),
        'progress_percent': ((current_index) / len(word_ids)) * 100,
    }
    return render(request, 'lessons/word_review.html', context)

@login_required
def user_progress(request):
    """Display user's overall progress"""
    progress = UserProgress.objects.filter(user=request.user).select_related('lesson')
    vocab_stats = WordKnowledgeService.get_user_vocabulary_stats(request.user)
    
    context = {
        'lesson_progress': progress,
        'vocab_stats': vocab_stats,
    }
    return render(request, 'lessons/user_progress.html', context)

@login_required
def vocabulary_stats(request):
    """Detailed vocabulary statistics"""
    stats = WordKnowledgeService.get_user_vocabulary_stats(request.user)
    word_knowledge = UserWordKnowledge.objects.filter(user=request.user).select_related('word')
    
    context = {
        'stats': stats,
        'word_knowledge': word_knowledge,
    }
    return render(request, 'lessons/vocabulary_stats.html', context)

@login_required
@require_POST
def submit_word_answer(request):
    """API endpoint for submitting word answers during review"""
    word_knowledge_id = request.POST.get('word_knowledge_id')
    is_correct = request.POST.get('is_correct') == 'true'
    response_time = request.POST.get('response_time_ms')
    
    # Get current review session
    session_id = request.session.get('review_session_id')
    if not session_id:
        return JsonResponse({'error': 'No active review session'}, status=400)
    
    session = get_object_or_404(ReviewSession, id=session_id, user=request.user)
    word_knowledge = get_object_or_404(UserWordKnowledge, id=word_knowledge_id, user=request.user)
    
    # Record the review
    ReviewSessionService.record_word_review(
        session, word_knowledge, is_correct, response_time
    )
    
    # Move to next word
    current_index = request.session.get('current_word_index', 0)
    request.session['current_word_index'] = current_index + 1
    
    return JsonResponse({
        'success': True,
        'next_word': current_index + 1 < len(request.session.get('review_words', []))
    })

@login_required
@require_POST
def complete_lesson_api(request):
    """API endpoint for completing a lesson"""
    lesson_id = request.POST.get('lesson_id')
    score = request.POST.get('score')
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    score = float(score) if score else None
    
    progress = LessonProgressService.complete_lesson(request.user, lesson, score)
    
    return JsonResponse({
        'success': True,
        'lesson_completed': True,
        'score': progress.score
    })
