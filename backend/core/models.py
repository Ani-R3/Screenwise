from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings

from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile
import os
import tempfile


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
    username = models.CharField(max_length=50, unique=False, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/ape2.jpg')
    bio = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    
# class Video(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     video_file = models.FileField(upload_to='videos/')
#     thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
#     ## Predefined category with dropdown choices 
#     category = models.CharField(max_length=100)
    
#     keywords = models.CharField(max_length=255, blank=True, help_text="Enter custom keywords, separated by commas.")
#     uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.title
    
#     ## for the Clean and normalize keywords
    
#     def save(self, *args, **kwargs):
#         if self.keywords:
#             self.keywords = ','.join([k.strip().lower() for k in self.keywords.split(',') if k.strip()])
        
#         super().save(*args, **kwargs)
        
        
#     def generate_thumbnail(self):
#         """
#         Generates a thumbnail from the 2nd second of the video.
#         NOTE: This requires the 'moviepy' library to be installed.
#         """
#         # This import would be at the top of your models.py file
#         # from moviepy.editor import VideoFileClip
#         # from django.core.files.base import ContentFile
#         # import os

#         try:
#             # Create a temporary path for the thumbnail
#             thumb_name = f"{os.path.basename(self.video_file.name)}.jpg"
#             thumb_path = os.path.join('/tmp', thumb_name)

#             # --- THIS IS THE PART THAT REQUIRES MOVIEPY ---
#             # with VideoFileClip(self.video_file.path) as clip:
#             #     clip.save_frame(thumb_path, t=2.00) # Save frame at 2 seconds
#             #
#             # with open(thumb_path, 'rb') as f:
#             #     self.thumbnail.save(thumb_name, ContentFile(f.read()), save=False)
#             #
#             # os.remove(thumb_path) # Clean up the temporary file
#             # super().save(update_fields=['thumbnail'])
            
#             # Placeholder message since we can't run the code above
#             print(f"Placeholder: Would generate thumbnail for {self.title} here.")
            
#         except Exception as e:
#             print(f"Error generating thumbnail for {self.title}: {e}")

        

class Video(models.Model):
    # These choices are for the new video_format field
    VIDEO_FORMAT_CHOICES = (
        ('standard', 'Standard'), # For horizontal, YouTube-style videos
        ('reel', 'Reel'),       # For vertical, Shorts/Reels-style videos
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, max_length=500)
    category = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255, blank=True, help_text="Enter custom keywords, separated by commas.")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    video_format = models.CharField(max_length=10, choices=VIDEO_FORMAT_CHOICES, default='standard')
    # Duration of the video in seconds
    duration = models.PositiveIntegerField(default=0, help_text="Duration in seconds")
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Custom save method to handle keyword cleaning and thumbnail generation.
        """
        # Save the model first to get a file path for the video
        # We use a flag to prevent recursion with the thumbnail generation
        is_new = self._state.adding
        super().save(*args, **kwargs)

        # After saving, if it's a new video and no thumbnail was provided, generate one.
        if is_new and self.video_file and not self.thumbnail:
            self.generate_thumbnail()
    
    def generate_thumbnail(self):
        """
        Generates a thumbnail from the 2nd second of the video using a secure temporary file.
        """
        try:
            # Use tempfile to create a secure temporary file with a .jpg suffix
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_thumb_path = temp_file.name

            # Use MoviePy to open the video and save a frame to our temporary path
            with VideoFileClip(self.video_file.path) as clip:
                clip.save_frame(temp_thumb_path, t=2.00) # Save frame at 2 seconds

            # Open the generated image file in binary-read mode
            with open(temp_thumb_path, 'rb') as f:
                # We set save=False to prevent this from calling the save() method again (infinite loop)
                self.thumbnail.save(
                    f"{os.path.basename(self.video_file.name)}.jpg",
                    ContentFile(f.read()),
                    save=False
                )

            os.remove(temp_thumb_path) # Clean up the temporary file

            # We call super().save() again, but we only update the 'thumbnail' field
            super().save(update_fields=['thumbnail'])
            
        except Exception as e:
            print(f"Error generating thumbnail for '{self.title}': {e}")    
