from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from core.models import Video
from recommendations.models import UserInteraction
from videos.forms import VideoEditForm

@login_required
def dashboard_view(request):
    user = request.user
    
    # --- 1. CREATOR ANALYTICS ---
    user_videos = Video.objects.filter(uploaded_by=user).order_by('-uploaded_at')
    total_views = user_videos.aggregate(total=Sum('views'))['total'] or 0
    subscriber_count = 1250 # Placeholder

    # --- 2. LEARNING JOURNEY & PRODUCTIVITY ---
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_interactions = UserInteraction.objects.filter(user=user, timestamp__gte=one_week_ago)

    PRODUCTIVE_CATEGORIES = ['productivity', 'education', 'tech', 'study']
    ENTERTAINMENT_CATEGORIES = ['entertainment', 'other'] 

    learning_seconds = 0
    entertainment_seconds = 0
    
    for interaction in recent_interactions:
        # Check if the video has a category before trying to access it
        if hasattr(interaction.video, 'category'):
            if interaction.video.category.lower() in PRODUCTIVE_CATEGORIES:
                learning_seconds += interaction.video.duration
            elif interaction.video.category.lower() in ENTERTAINMENT_CATEGORIES:
                entertainment_seconds += interaction.video.duration

    total_watch_seconds = learning_seconds + entertainment_seconds
    productivity_score = int((learning_seconds / total_watch_seconds) * 100) if total_watch_seconds > 0 else 0
    
    context = {
        'user_videos': user_videos,
        'creator_stats': {
            'total_videos': user_videos.count(),
            'total_views': total_views,
            'subscriber_count': subscriber_count,
        },
        'learning_stats': {
            'videos_watched_this_week': recent_interactions.count(),
            'learning_hours_this_week': learning_seconds / 3600,
            'entertainment_hours_this_week': entertainment_seconds / 3600,
            'get_productivity_score': productivity_score,
            'current_streak_days': 14, # Placeholder
            'completion_rate': 85, # Placeholder
        },
        'recent_activities': recent_interactions.order_by('-timestamp')[:5], 
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def video_edit_view(request, video_id):
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)
    if request.method == 'POST':
        form = VideoEditForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video updated successfully!')
            return redirect('dashboard:dashboard')
    else:
        form = VideoEditForm(instance=video)
    return render(request, 'dashboard/video_edit_form.html', {'form': form, 'video': video})
@login_required
def video_delete_view(request, video_id):
    """
    Handles the deletion of a video, including its database record
    AND its associated media files.
    """
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user) # Security check
    
    if request.method == 'POST':
        # 1. Delete the actual video and thumbnail files from storage
        #    It's good practice to do this before deleting the database record.
        if video.video_file:
            video.video_file.delete(save=False)
        if video.thumbnail:
            video.thumbnail.delete(save=False)

        # 2. Now, delete the video record from the database
        video.delete()
        
        messages.success(request, 'Video was deleted successfully.')
    
    return redirect('dashboard:dashboard')
