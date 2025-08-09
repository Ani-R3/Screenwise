from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.db.models import Q

User = get_user_model()  # This now points to core.CustomUser

def login_view(request):
    if request.method == "POST":
        login_input = request.POST.get('username')
        password = request.POST.get('password')

        # Allow both username and email login
        try:
            user_obj = User.objects.get(Q(username=login_input) | Q(email=login_input))
            username = user_obj.username
        except User.DoesNotExist:
            username = login_input

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username/email or password.")
            
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
