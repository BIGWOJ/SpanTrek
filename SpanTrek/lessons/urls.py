from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('world_map/', views.world_map, name='world_map'),
    path('<str:country>/', views.country_view, name='country_map'),
    path('<str:country>/<str:landmark>/', views.country_landmark_lesson, name='country_landmark_lesson'),
    path('<str:country>/<str:landmark>/<int:lesson_number>/', views.country_landmark_lesson, name='landmark_lesson_with_number'),
    path('<str:country>/<str:landmark>/<int:lesson_number>/<int:exercise_number>/', views.country_landmark_lesson, name='landmark_lesson_with_exercise'),
    path('<str:country>/<str:landmark>/<int:lesson_number>/complete/', views.lesson_complete, name='lesson_complete'),
]