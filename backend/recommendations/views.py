# from django.shortcuts import render

# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
# from .models import UserInteraction
# from core.models import Video
# import json

# @login_required
# @require_POST
# def track_view(request):
#     """
#     An API endpoint to record a video view interaction.
#     """
#     try:
#         data = json.loads(request.body)
#         video_id = data.get('video_id')
#         if video_id:
#             video = Video.objects.get(id=video_id)
#             # Create or update the interaction record
#             UserInteraction.objects.update_or_create(
#                 user=request.user, 
#                 video=video, 
#                 interaction_type='view'
#             )
#             return JsonResponse({'status': 'ok'})
#     except (json.JSONDecodeError, Video.DoesNotExist):
#         pass
#     return JsonResponse({'status': 'error'}, status=400)



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import UserInteraction
from core.models import Video
import json

@login_required
@require_POST
def track_view(request):
    try:
        data = json.loads(request.body)
        video_id = data.get('video_id')
        if video_id:
            video = Video.objects.get(id=video_id)
            UserInteraction.objects.update_or_create(
                user=request.user, 
                video=video, 
                interaction_type='view'
            )
            return JsonResponse({'status': 'ok'})
    except (json.JSONDecodeError, Video.DoesNotExist):
        pass
    return JsonResponse({'status': 'error'}, status=400)