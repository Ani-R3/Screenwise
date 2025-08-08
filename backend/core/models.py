from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(email, username, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/avtar.svg')
    bio = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    ## Predefined category with dropdown choices 
    category = models.CharField(max_length=100, choices=[
        ('productivity', 'Productivity'),
        ('education', 'Education'),
        ('tech', 'Tech'),
        ('study', 'Study'),
        ('other', 'Other')
    ])
    
    keywords = models.CharField(max_length=255, blank=True, help_text="Enter custom keywords, separated by commas.")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    ## for the Clean and normalize keywords
    
    def save(self, *args, **kwargs):
        if self.keywords:
            self.keywords = ','.join([k.strip().lower() for k in self.keywords.split(',') if k.strip()])
        
        super().save(*args, **kwargs)
        
