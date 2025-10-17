
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),  # Include the base app's URLs
    path("lessons/", include("lessons.urls")),  # Include the lessons app's URLs
    path("practice/", include("practice.urls")),  # Include the practice app's URLs
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
