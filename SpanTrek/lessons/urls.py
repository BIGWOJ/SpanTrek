from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('world_map/', views.world_map, name='world_map'),
    path('spain/', views.country_view, {'country': 'spain'}, name='spain'),
    path('peru/', views.country_view, {'country': 'peru'}, name='peru'),
    path('mexico/', views.country_view, {'country': 'mexico'}, name='mexico'),
    path('poland/', views.country_view, {'country': 'poland'}, name='poland'),
    # landmark-specific lesson URLs
    path('<str:country>/<str:landmark>/', views.country_landmark_lesson, name='country_landmark_lesson'),
    path('<str:country>/<str:landmark>/<int:lesson_number>/', views.country_landmark_lesson, name='landmark_lesson_with_number'),
]