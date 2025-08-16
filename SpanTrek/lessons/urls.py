from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('world-map/', views.world_map, name='world_map'),
]
