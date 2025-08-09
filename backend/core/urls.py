from django.urls import path, include
from core import views

urlpatterns = [
    path('login/',views.login, name = 'login'), 
    path('home/', views.home, name="home"),
    path('upload/',views.upload_video, name='upload'),
    path('dashboard/',views.dashboard_page, name='dashboard')
]
