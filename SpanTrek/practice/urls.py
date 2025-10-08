from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('intro/<str:practice_type>', views.practice_intro, name='practice_intro'),
]