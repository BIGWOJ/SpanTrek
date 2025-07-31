from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
]