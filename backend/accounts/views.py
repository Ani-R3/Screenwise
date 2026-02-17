# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.db.models import Q
# from django.contrib.auth import get_user_model

# User = get_user_model()

# def login_view(request):
#     if request.method == "POST":
#         login_input = request.POST.get('username')  # can be email or username
#         password = request.POST.get('password')

#         try:
#             # Find the user by username or email
#             user_obj = User.objects.get(Q(username=login_input) | Q(email=login_input))
#             email = user_obj.email  # always use email for authentication
#         except User.DoesNotExist:
#             email = login_input  # if user typed their email directly

#         # Authenticate using email (USERNAME_FIELD)
#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')  # change to your dashboard route name
#         else:
#             messages.error(request, "Invalid username/email or password.")

#     return render(request, 'auth/login.html')



    
    
    
# #--------------------------
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# # 🚨 New Import: Use the standard form for reliable validation
# # from django.contrib.auth.forms import AuthenticationForm 
# # from django.contrib.auth.forms import UserCreationForm 

# from accounts.forms import LoginForm, CustomUserCreationForm 


# # You can keep Q, get_user_model, and User if needed for other parts of the app, 
# # but they are not needed for this simplified login_view.

# # accounts/views.py (inside login_view)

# def login_view(request):
#     if request.method == "POST":
#         # 🚨 FIX: Use your custom LoginForm
#         form = LoginForm(request.POST) 

#         if form.is_valid():
#             # The LoginForm has a get_user() method built-in
#             user = form.get_user() 
#             login(request, user)
            
#             # ... (rest of the redirect logic is fine)
#             next_url = request.GET.get('next') or 'accounts:dashboard' # Use accounts:dashboard
            
#             messages.success(request, f"Welcome back, {user.username}!")
#             return redirect(next_url)
#         else:
#             messages.error(request, "Invalid username/email or password.")

#     else:
#         # 🚨 FIX: Instantiate your custom LoginForm
#         form = LoginForm()

#     return render(request, 'core/templates/auth/login.html', {'form': form}) 
#     # Note: Use the full template path or ensure Django can find 'auth/login.html'

# # (Keep your logout_view as it is fine)

# def logout_view(request):
#     logout(request)
#     return redirect('login')



# def signup_view(request):
#     if request.method == 'POST':
#         # Use Django's built-in form or your custom form here
#         form = UserCreationForm(request.POST) 
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created successfully! Please log in.')
#             return redirect('login') # Redirect to the login page
#         else:
#             # If validation fails (e.g., passwords don't match, username exists)
#             messages.error(request, 'Sign up failed. Check form errors.')
#     else:
#         form = UserCreationForm()
        
#     return redirect('login') from django.shortcuts import render, redirect# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginForm, CustomUserCreationForm

# --- Combined Login and Sign Up View ---
def login_signup_view(request):
    """
    Handles both user login and signup on the same page.
    """
    # Initialize both forms
    login_form = LoginForm()
    signup_form = CustomUserCreationForm()
    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }

    if request.method == 'POST':
        # Check which form was submitted. We'll check the name of the submit button.
        if 'login_submit' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                # next_url = request.GET.get('next', 'dashboard')
                # return redirect(next_url)
                return redirect('profiles:profile', username=user.username)
            else:
                # Failed login, update the context with the errored form
                context['login_form'] = login_form

        elif 'signup_submit' in request.POST:
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('accounts:login')
            else:
                # Failed signup, update context and flag for JS
                context['signup_form'] = signup_form
                context['signup_error'] = True

    return render(request, 'auth/login.html', context)


# --- LOGOUT VIEW ---
def logout_view(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    return redirect('accounts:login')

# accounts/views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout
# from django.contrib import messages
# from .forms import LoginForm, CustomUserCreationForm

# def login_signup_view(request):
#     login_form = LoginForm()
#     signup_form = CustomUserCreationForm()
#     context = {
#         'login_form': login_form,
#         'signup_form': signup_form,
#     }

#     if request.method == 'POST':
#         # --- DEBUG: Print all data received from the form ---
#         print("---------- FORM SUBMITTED ----------")
#         print(request.POST)
#         print("---------------------------------")
#         # ----------------------------------------------------

#         if 'signup_submit' in request.POST:
#             # --- DEBUG: Check if we entered the signup block ---
#             print("✅ Correctly identified SIGNUP form submission.")
#             # ----------------------------------------------------
            
#             signup_form = CustomUserCreationForm(request.POST)
#             if signup_form.is_valid():
#                 # --- DEBUG: Check if the form is valid ---
#                 print("✅ Signup form is VALID. Saving user...")
#                 # -----------------------------------------
                
#                 signup_form.save()
#                 messages.success(request, 'Account created successfully! Please log in.')
#                 return redirect('accounts:login')
#             else:
#                 # --- DEBUG: If form is invalid, print the errors ---
#                 print("❌ Signup form is INVALID. Errors:")
#                 print(signup_form.errors)
#                 # ----------------------------------------------------
                
#                 context['signup_form'] = signup_form
#                 context['signup_error'] = True
        
#         # (The login logic can stay the same)
#         elif 'login_submit' in request.POST:
#             login_form = LoginForm(request.POST)
#             if login_form.is_valid():
#                 user = login_form.get_user()
#                 login(request, user)
#                 messages.success(request, f"Welcome back, {user.username}!")
#                 next_url = request.GET.get('next', 'dashboard')
#                 return redirect(next_url)
#             else:
#                 context['login_form'] = login_form

#     return render(request, 'auth/login.html', context)

# # (logout_view stays the same)
# def logout_view(request):
#     logout(request)
#     return redirect('accounts:login')