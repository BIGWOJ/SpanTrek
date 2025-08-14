from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from .models import (
    UserWordKnowledge, UserProgress, UserListeningProgress, UserReadingProgress,
    ReviewSession, WordReview, Word
)

class LessonProgressService:
    """Service class for managing user lesson progress"""
    
    @staticmethod
    def start_lesson(user, lesson):
        """Initialize or get user progress for a lesson"""
        progress, created = UserProgress.objects.get_or_create(
            user=user,
            lesson=lesson,
            defaults={'started_at': timezone.now()}
        )
        if not created:
            progress.last_accessed = timezone.now()
            progress.save()
        return progress
    
    @staticmethod
    def complete_lesson(user, lesson, score=None):
        """Mark lesson as completed and update user stats"""
        with transaction.atomic():
            progress = UserProgress.objects.get(user=user, lesson=lesson)
            progress.is_completed = True
            progress.completion_date = timezone.now()
            if score is not None:
                progress.score = score
            progress.save()
            
            # Update user's overall stats
            user.words_learned = UserWordKnowledge.objects.filter(
                user=user, 
                knowledge_level__in=['known', 'mastered']
            ).count()
            user.save()
            
        return progress

class WordKnowledgeService:
    """Service for managing word knowledge and spaced repetition"""
    
    # Spaced repetition intervals (in days)
    INTERVALS = {
        'unknown': 1,
        'learning': 3,
        'familiar': 7,
        'known': 14,
        'mastered': 30
    }
    
    @staticmethod
    def update_word_knowledge(user, word, is_correct):
        """Update word knowledge based on user response"""
        knowledge, created = UserWordKnowledge.objects.get_or_create(
            user=user,
            word=word,
            defaults={'knowledge_level': 'unknown'}
        )
        
        knowledge.last_reviewed = timezone.now()
        knowledge.review_count += 1
        
        if is_correct:
            knowledge.correct_streak += 1
            # Progress to next level
            if knowledge.knowledge_level == 'unknown':
                knowledge.knowledge_level = 'learning'
            elif knowledge.knowledge_level == 'learning' and knowledge.correct_streak >= 2:
                knowledge.knowledge_level = 'familiar'
            elif knowledge.knowledge_level == 'familiar' and knowledge.correct_streak >= 3:
                knowledge.knowledge_level = 'known'
            elif knowledge.knowledge_level == 'known' and knowledge.correct_streak >= 5:
                knowledge.knowledge_level = 'mastered'
        else:
            knowledge.correct_streak = 0
            # Regress if necessary
            if knowledge.knowledge_level in ['known', 'mastered']:
                knowledge.knowledge_level = 'familiar'
            elif knowledge.knowledge_level == 'familiar':
                knowledge.knowledge_level = 'learning'
        
        # Set next review date
        interval_days = WordKnowledgeService.INTERVALS.get(knowledge.knowledge_level, 1)
        knowledge.next_review_date = timezone.now() + timedelta(days=interval_days)
        
        knowledge.save()
        return knowledge
    
    @staticmethod
    def get_words_for_review(user, limit=20):
        """Get words due for review"""
        return UserWordKnowledge.objects.filter(
            user=user,
            next_review_date__lte=timezone.now()
        ).select_related('word').order_by('next_review_date')[:limit]
    
    @staticmethod
    def get_user_vocabulary_stats(user):
        """Get vocabulary statistics for a user"""
        knowledge_queryset = UserWordKnowledge.objects.filter(user=user)
        
        return {
            'total_words': knowledge_queryset.count(),
            'unknown': knowledge_queryset.filter(knowledge_level='unknown').count(),
            'learning': knowledge_queryset.filter(knowledge_level='learning').count(),
            'familiar': knowledge_queryset.filter(knowledge_level='familiar').count(),
            'known': knowledge_queryset.filter(knowledge_level='known').count(),
            'mastered': knowledge_queryset.filter(knowledge_level='mastered').count(),
            'due_for_review': knowledge_queryset.filter(next_review_date__lte=timezone.now()).count()
        }

class ReviewSessionService:
    """Service for managing review sessions"""
    
    @staticmethod
    def start_review_session(user, session_type):
        """Start a new review session"""
        return ReviewSession.objects.create(
            user=user,
            session_type=session_type
        )
    
    @staticmethod
    def complete_review_session(session):
        """Complete a review session"""
        session.completed_at = timezone.now()
        session.save()
        return session
    
    @staticmethod
    def record_word_review(session, word_knowledge, is_correct, response_time_ms=None):
        """Record a word review within a session"""
        with transaction.atomic():
            # Update session stats
            session.total_items += 1
            if is_correct:
                session.correct_answers += 1
            session.save()
            
            # Create word review record
            word_review = WordReview.objects.create(
                session=session,
                word_knowledge=word_knowledge,
                is_correct=is_correct,
                response_time_ms=response_time_ms
            )
            
            # Update word knowledge
            WordKnowledgeService.update_word_knowledge(
                word_knowledge.user,
                word_knowledge.word,
                is_correct
            )
            
            return word_review

class ContentRecommendationService:
    """Service for recommending content based on user progress"""
    
    @staticmethod
    def get_recommended_words(user, limit=10):
        """Get recommended words for learning"""
        # Get words user hasn't seen or needs review
        known_words = UserWordKnowledge.objects.filter(user=user).values_list('word_id', flat=True)
        
        queryset = Word.objects.exclude(id__in=known_words)
        
        return queryset.order_by('?')[:limit]  # Random selection
    
    @staticmethod
    def get_next_lesson_recommendation(user):
        """Recommend next lesson based on user progress"""
        from .models import Lesson
        
        # Get completed lessons
        completed_lessons = UserProgress.objects.filter(
            user=user, 
            is_completed=True
        ).values_list('lesson_id', flat=True)
        
        # Get next lesson in sequence
        next_lesson = Lesson.objects.filter(
            is_active=True
        ).exclude(id__in=completed_lessons).order_by('order').first()
        
        return next_lesson
    
    @staticmethod
    def should_user_review(user):
        """Check if user has words due for review"""
        due_count = UserWordKnowledge.objects.filter(
            user=user,
            next_review_date__lte=timezone.now()
        ).count()
        
        return due_count > 0, due_count
