from django.urls import path
from .views import upload_video_view, video_detail_view

app_name = 'videos'

urlpatterns = [
    path('upload/', upload_video_view, name='upload'),
    path('video/<int:video_id>/', video_detail_view, name='video_detail'),
]