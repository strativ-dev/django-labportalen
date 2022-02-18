# Django import
from django.urls import path, include
# Self import

urlpatterns = [
    path('api/', include('labportalen.api.urls')),
]
