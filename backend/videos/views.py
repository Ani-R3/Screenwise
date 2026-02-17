from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import VideoUploadForm
from core.models import Video
from moviepy.editor import VideoFileClip

@login_required
def upload_video_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.uploaded_by = request.user
            
            # --- THIS IS THE NEW AUTOMATION LOGIC ---
            new_video.save() 
            
            try:
                # Use moviepy to open the video file from its path
                with VideoFileClip(new_video.video_file.path) as clip:
                    new_video.duration = int(clip.duration)
                    width, height = clip.size
                    
                    if height > width:
                        new_video.video_format = 'reel'
                    else:
                        new_video.video_format = 'standard'
                
                # Save the video object again with the new data
                new_video.save(update_fields=['duration', 'video_format'])

            except Exception as e:
                print(f"Error processing video metadata for {new_video.title}: {e}")

            messages.success(request, 'Your video has been uploaded successfully!')
            return redirect('profiles:profile', username=request.user.username)
    else:
        form = VideoUploadForm()
        
    return render(request, 'videos/upload_video.html', {'form': form})

def video_detail_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.views += 1
    video.save(update_fields=['views'])
    context = {
        'video': video
    }
    return render(request, 'videos/video_detail.html', context)