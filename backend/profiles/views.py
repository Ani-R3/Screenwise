from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from core.models import Video 
from .forms import ProfileUpdateForm

User = get_user_model()

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username__iexact=username)
    uploaded_videos = Video.objects.filter(uploaded_by=profile_user).order_by('-uploaded_at')
    is_owner = (request.user == profile_user)
    
    if is_owner and request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profiles:profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile_user)

    context = {
        'profile_user': profile_user,
        'uploaded_videos': uploaded_videos,
        'is_owner': is_owner,
        'form': form
    }
    
    return render(request, 'profiles/profile.html', context)