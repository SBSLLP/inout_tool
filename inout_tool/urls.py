# inout_tool/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('checkin.urls')),  # Include your app URLs
]
