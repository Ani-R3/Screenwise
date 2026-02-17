# app_name = 'accounts'

# from django.urls import path
# from accounts.views import login_view, logout_view, signup_view

# urlpatterns = [
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
#     path('signup/', signup_view, name='signup'),
# ]


# accounts/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import login_signup_view, logout_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_signup_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            # This new line tells the view where to go after sending the email
            success_url=reverse_lazy('accounts:password_reset_done')
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            # We add a success_url here too for after the password is changed
            success_url=reverse_lazy('accounts:password_reset_complete')
         ), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), 
         name='password_reset_complete'),
]

