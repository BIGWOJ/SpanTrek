from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    # Lesson URLs
    path('', views.lesson_list, name='lesson_list'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/start/', views.start_lesson, name='start_lesson'),
    
    # Review URLs
    path('review/', views.review_dashboard, name='review_dashboard'),
    path('review/words/', views.word_review_session, name='word_review'),
    
    # Progress URLs
    path('progress/', views.user_progress, name='user_progress'),
    path('vocabulary/', views.vocabulary_stats, name='vocabulary_stats'),
    
    # API endpoints for AJAX calls
    path('api/word-answer/', views.submit_word_answer, name='submit_word_answer'),
    path('api/lesson-complete/', views.complete_lesson_api, name='complete_lesson_api'),
]
