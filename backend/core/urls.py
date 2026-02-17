

from django.urls import path, include
from core import views
from .views import home_view

app_name = 'core'



urlpatterns = [
    #path('login/',views.login, name = 'login'),
    #path('home/', views.home, name="home"),
    path('', home_view, name='home'),
    # path('upload/',views.upload_video, name='upload'),
    #path('dashboard/',views.dashboard_page, name='dashboard')
]
