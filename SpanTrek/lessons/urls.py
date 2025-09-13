from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('world_map/', views.world_map, name='world_map'),
    path('spain/', views.country_view, {'country': 'spain'}, name='spain'),
    path('peru/', views.country_view, {'country': 'peru'}, name='peru'),
    path('mexico/', views.country_view, {'country': 'mexico'}, name='mexico'),
    path('poland/', views.country_view, {'country': 'poland'}, name='poland'),
    # City-specific lesson URLs
    path('<str:country>/<str:city>/', views.country_city_lesson, name='country_city_lesson'),
    path('<str:country>/<str:city>/<int:lesson_number>/', views.country_city_lesson, name='city_lesson_with_number'),
]