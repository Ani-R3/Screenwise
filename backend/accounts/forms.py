from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import Q

# Use get_user_model() to get the correct swapped model reference
User = get_user_model() 

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your email or username",
            "class": "w-full h-12 px-3 py-2 border border-gray-300 rounded-lg"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "w-full h-12 px-3 py-2 border border-gray-300 rounded-lg"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        login_input = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if login_input and password:
            try:
                # Find the user by username OR email (case-insensitive lookup)
                user_obj = User.objects.get(Q(username__iexact=login_input) | Q(email__iexact=login_input))
                username = user_obj.username
            except User.DoesNotExist:
                # If user not found by email/username, let authentication handle the failure
                username = login_input 

            # Authenticate using the retrieved username
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username/email or password.")
            
            # CRUCIAL: Store the user object for retrieval by the view
            self.user = user
            
        return cleaned_data

    # 🚨 FIX for views.py: Implement the required get_user() method 🚨
    def get_user(self):
        """Returns the user object authenticated by clean()."""
        # This relies on self.user being set in the clean() method above.
        return self.user

# --- Sign Up Forms ---

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        required=True
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}),
        required=True
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')

    # 🚨 ADD THIS ENTIRE METHOD 🚨
    def clean_username(self):
        """
        This method checks if a user with the given email already exists.
        """
        # Get the email from the form's data
        email = self.cleaned_data.get('username')
        
        # Check case-insensitively if a user exists with this username or email
        if User.objects.filter(Q(username__iexact=email) | Q(email__iexact=email)).exists():
            raise forms.ValidationError("A user with this email already exists.")
        
        # If no user is found, return the email
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set both username and email to the provided email address
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['username']
        if commit:
            user.save()
        return user

