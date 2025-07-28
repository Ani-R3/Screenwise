from django.urls import path, include
from core import views

urlpatterns = [
    path('login/',views.login, name = 'login'),   
]
