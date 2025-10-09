from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('intro/<str:practice_type>', views.practice_intro, name='practice_intro'),
    path('main/<int:index>', views.practice_main, name='practice_main'),
    path('complete/', views.practice_complete, name='practice_complete'),
]