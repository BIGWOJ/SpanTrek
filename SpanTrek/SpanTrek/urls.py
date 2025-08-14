
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),  # Include the base app's URLs
    path("lessons/", include("lessons.urls")),  # Include the lessons app's URLs
]
