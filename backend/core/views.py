from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 
##This imports the model that stores OAuth login 
# information per user (like access tokens, provider name, user IDs
from social_django.models import UserSocialAuth
from .models import Video
from recommendations.services import get_recommendations


def home_view(request):
    """
    A simplified view that ALWAYS fetches all videos and separates them
    into 'reels' and 'standard_videos' for display.
    """
    # This directly fetches ALL videos from the database, ignoring recommendations
    all_videos = Video.objects.all().order_by('-uploaded_at')

    # Separate them into two lists for the template
    reels = all_videos.filter(video_format='reel')[:7]
    standard_videos = all_videos.filter(video_format='standard')

    context = {
        'reels': reels,
        'standard_videos': standard_videos,
    }
    return render(request, 'home.html', context)
# def home_view(request):
#     """
#     Shows personalized recommendations to logged-in users,
#     and the latest videos to guests.
#     """
#     if request.user.is_authenticated:
#         # For logged-in users, get personalized recommendations
#         videos = get_recommendations(request.user)
#     else:
#         # For guests, just show the latest videos
#         videos = Video.objects.all().order_by('-uploaded_at')[:20]

#     context = {
#         'videos': videos
#     }
#     return render(request, 'home.html', context)




# def login(request):
#     text = "hello ji"
#     template = loader.get_template('auth/login.html')
#     context  = {'text' : text}
#     res = template.render(context, request)
#    return HttpResponse(res)

# def login(request):
#     return render(request, 'auth/login.html', {'text': 'Home'})



## returning home 
def home(request):
    return render(request,'home.html')


##returning upload

# def upload_video(request):
#     return render(request, 'videos/uploads.html')


##returning the dashboard
def dashboard_page(request):
    return render(request, 'dashboard.html')


##fuction for getting the youtube data
def get_youtube_data(request):
    """
    View to fetch YouTube channel data of the logged-in user using Google OAuth2 access token.
    Assumes the user has logged in via Google and granted YouTube access.
    """
    
    ## Gets the currently logged-in Django user.
    user = request.user
    ##This gets the social login record associated with the user where the provider is 'google-oauth2'.
    google_login = user.social_auth.get(provider='google-oauth2')
    
    #access_token = google_login.extra_data[access_token]
    
    
#def get_watch_history(token):
    