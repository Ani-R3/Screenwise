# from django.db import models

# from django.db import models
# from django.conf import settings
# from core.models import Video

# class UserInteraction(models.Model):
#     """
#     Tracks interactions a user has with a video.
#     This is the foundation of our recommendation engine.
#     """
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     # We can add 'like', 'share' etc. later
#     interaction_type = models.CharField(max_length=10, default='view')
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         # A user can view the same video multiple times, but we only care about the latest view for now
#         unique_together = ('user', 'video', 'interaction_type')

#     def __str__(self):
#         return f"{self.user.username} - {self.interaction_type} - {self.video.title}"



from django.db import models
from django.conf import settings
from core.models import Video

class UserInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, default='view')
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'video', 'interaction_type')

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.video.title}"