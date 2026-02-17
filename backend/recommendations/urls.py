from django.urls import path
from .views import track_view

app_name = 'recommendations'

urlpatterns = [
    path('track_view/', track_view, name='track_view'),
]
