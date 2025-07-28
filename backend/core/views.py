from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 
##This imports the model that stores OAuth login 
# information per user (like access tokens, provider name, user IDs
from social_django.models import UserSocialAuth



def login(request):
    text = "hello ji"
    template = loader.get_template('login.html')
    context  = {'text' : text}
    res = template.render(context, request)
    
    return HttpResponse(res)
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
    