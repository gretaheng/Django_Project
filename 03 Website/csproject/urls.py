# Original code

from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('visual_crime/', include('visual_crime.urls')),
    path('route/', include('route.urls')),
    path('analysis/', include('analysis.urls')),
    path('home/', include('home.urls')),
    path('route/map/', include('route.urls')),
]
