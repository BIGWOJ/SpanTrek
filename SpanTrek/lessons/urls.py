from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('world-map/', views.world_map, name='world_map'),
    path('spain/', views.spain_view, name='spain'),
    path('peru/', views.peru_view, name='peru'),
    path('mexico/', views.mexico_view, name='mexico'),
]
