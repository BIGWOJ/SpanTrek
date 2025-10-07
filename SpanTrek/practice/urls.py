from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('random/', views.random_practice, name='random_practice'),
]