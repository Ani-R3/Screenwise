from django.urls import path
from .views import dashboard_view, video_edit_view, video_delete_view

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard page (e.g., /dashboard/)
    path('', dashboard_view, name='dashboard'),
    
    # Page to edit a specific video (e.g., /dashboard/edit/5/)
    path('edit/<int:video_id>/', video_edit_view, name='video_edit'),
    
    # URL to handle deleting a video (e.g., /dashboard/delete/5/)
    path('delete/<int:video_id>/', video_delete_view, name='video_delete'),
]