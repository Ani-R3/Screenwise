# from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer
# from core.models import Video
# from .models import UserInteraction
# import numpy as np

# # Load a pre-trained model. This will download the model the first time it's run.
# # 'all-MiniLM-L6-v2' is a small but powerful model for sentence similarity.
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # In a production system, these embeddings would be pre-calculated and stored.
# # For simplicity, we'll cache them in memory.
# video_embeddings_cache = {}

# def get_all_video_embeddings():
#     """
#     Generates or retrieves embeddings for all videos in the database.
#     """
#     if not video_embeddings_cache:
#         print("Generating and caching all video embeddings...")
#         videos = Video.objects.all()
#         video_texts = [f"{v.title} {v.description} {v.keywords}" for v in videos]
#         embeddings = model.encode(video_texts, convert_to_tensor=False)
#         for i, video in enumerate(videos):
#             video_embeddings_cache[video.id] = embeddings[i]
#     return video_embeddings_cache

# def get_recommendations(user):
#     """
#     Generates personalized video recommendations for a given user.
#     """
    
#     print(f"--- Running recommendations for user: {user.username} ---") 
    
#     # 1. Get all video embeddings
#     all_embeddings = get_all_video_embeddings()
#     if not all_embeddings:
#         # Fallback for when there are no videos
#         return Video.objects.none()

#     # 2. Get the user's recent watch history
#     recent_views = UserInteraction.objects.filter(user=user, interaction_type='view').order_by('-timestamp')[:10]
#     watched_video_ids = [view.video_id for view in recent_views]

#     print(f"DEBUG: User has watched these videos: {watched_video_ids}") # DEBUG


#     if not watched_video_ids:
#         print("DEBUG: Cold Start! User has no watch history. Fetching latest videos.") # DEBUG
#         # "Cold Start" problem: If user has no history, return latest videos but exclude watched ones.
#         return Video.objects.exclude(id__in=watched_video_ids).order_by('-uploaded_at')

#     # 3. Create a user "interest" profile
#     # We'll average the embeddings of the videos they've watched.
#     user_interest_vectors = [all_embeddings[vid] for vid in watched_video_ids if vid in all_embeddings]
#     if not user_interest_vectors:
#          return Video.objects.exclude(id__in=watched_video_ids).order_by('-uploaded_at')

#     user_profile = np.mean(user_interest_vectors, axis=0).reshape(1, -1)
    
#     # 4. Calculate similarity between the user's profile and all videos
#     video_ids = list(all_embeddings.keys())
#     all_video_vectors = np.array([all_embeddings[vid] for vid in video_ids])
    
#     similarities = cosine_similarity(user_profile, all_video_vectors)[0]
    
#     # 5. Get the most similar videos
#     # Pair each video with its similarity score
#     scored_videos = sorted(zip(video_ids, similarities), key=lambda x: x[1], reverse=True)
    
#     # Filter out videos the user has already watched
#     recommended_ids = [vid for vid, score in scored_videos if vid not in watched_video_ids]
    
#     # Fetch the recommended video objects from the database, preserving the order of recommendation
#     recommended_videos = list(Video.objects.filter(id__in=recommended_ids))
#     recommended_videos.sort(key=lambda v: recommended_ids.index(v.id))
    
#     return recommended_videos[:12] # Return the top 12 recommendations



# from django.core.cache import cache
# from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer
# from core.models import Video
# from .models import UserInteraction
# import numpy as np

# # --- Helper functions for AI model and embeddings ---

# def get_sentence_transformer_model():
#     """Loads the pre-trained AI model. Caches it for efficiency."""
#     model_name = 'all-MiniLM-L6-v2'
#     # Try to get the model from cache first
#     model = cache.get(model_name)
#     if model is None:
#         # If not in cache, load the model and cache it for 24 hours
#         model = SentenceTransformer(model_name)
#         cache.set(model_name, model, 60 * 60 * 24)
#     return model

# def get_video_embeddings(video_ids):
#     """Generates numerical representations (embeddings) for a list of videos."""
#     videos = Video.objects.filter(id__in=video_ids)
#     if not videos:
#         return {}
    
#     # Combine the text from title, description, and keywords
#     texts_to_embed = [
#         f"{v.title}. {v.description} Keywords: {v.keywords}" for v in videos
#     ]
#     model = get_sentence_transformer_model()
#     embeddings = model.encode(texts_to_embed)
    
#     return {video.id: embedding for video, embedding in zip(videos, embeddings)}

# def get_all_video_embeddings():
#     """
#     Gets embeddings for all videos. Uses caching to avoid regenerating them
#     on every request, making the site much faster.
#     """
#     cache_key = 'all_video_embeddings'
#     all_embeddings = cache.get(cache_key)
    
#     if all_embeddings is None:
#         print("Generating and caching all video embeddings...") # For debugging
#         all_embeddings = get_video_embeddings(Video.objects.values_list('id', flat=True))
#         # Cache the embeddings for 1 hour
#         cache.set(cache_key, all_embeddings, 60 * 60)
        
#     return all_embeddings


# # --- The main recommendation function ---

# def get_recommendations(user):
#     """
#     Generates personalized video recommendations for a user.
#     - If the user has a watch history, it finds videos similar to what they've watched.
#     - If the user has no history (cold start), it returns the latest videos.
#     - If no new recommendations are found, it falls back to the latest videos.
#     """
#     all_embeddings = get_all_video_embeddings()
#     if not all_embeddings:
#         return Video.objects.none() # Return empty if no videos exist at all

#     video_ids, embeddings_matrix = zip(*all_embeddings.items())
#     embeddings_matrix = np.array(embeddings_matrix)

#     # Get the last 10 videos the user has viewed
#     recent_views = UserInteraction.objects.filter(user=user, interaction_type='view').order_by('-timestamp')[:10]
#     watched_video_ids = {view.video_id for view in recent_views}

#     if not watched_video_ids:
#         # "Cold Start" problem: User has no history, so return the latest videos
#         return Video.objects.all().order_by('-uploaded_at')[:20]

#     # Create an average "interest" vector from the videos the user has watched
#     watched_embeddings = [all_embeddings[vid] for vid in watched_video_ids if vid in all_embeddings]
#     if not watched_embeddings:
#          return Video.objects.all().order_by('-uploaded_at')[:20]

#     user_interest_vector = np.mean(watched_embeddings, axis=0).reshape(1, -1)

#     # Calculate similarity between the user's interest and all other videos
#     similarities = cosine_similarity(user_interest_vector, embeddings_matrix)[0]
    
#     # Get the indices of the most similar videos in descending order
#     sorted_indices = np.argsort(similarities)[::-1]
    
#     # Filter out videos the user has already watched to avoid recommending them again
#     recommended_ids = [video_ids[i] for i in sorted_indices if video_ids[i] not in watched_video_ids]

#     # If, after filtering, we have no new recommendations, fall back to the latest videos
#     if not recommended_ids:
#         # Fallback: Simply return all videos, ordered by latest.
#         # The template will still show a grid, just not a personalized one.
#         return Video.objects.all().order_by('-uploaded_at')[:20]

#     # Get the actual Video objects from the database, preserving the recommendation order
#     recommended_videos = list(Video.objects.filter(id__in=recommended_ids[:20]))
#     recommended_videos.sort(key=lambda x: recommended_ids.index(x.id))
    
#     return recommended_videos


from django.core.cache import cache
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from core.models import Video
from .models import UserInteraction
import numpy as np

def get_sentence_transformer_model():
    model_name = 'all-MiniLM-L6-v2'
    model = cache.get(model_name)
    if model is None:
        model = SentenceTransformer(model_name)
        cache.set(model_name, model, 60 * 60 * 24)
    return model

def get_all_video_embeddings():
    cache_key = 'all_video_embeddings'
    all_embeddings = cache.get(cache_key)
    if all_embeddings is None:
        videos = Video.objects.all()
        texts_to_embed = [f"{v.title}. {v.description} {v.keywords}" for v in videos]
        model = get_sentence_transformer_model()
        embeddings = model.encode(texts_to_embed)
        all_embeddings = {video.id: embedding for video, embedding in zip(videos, embeddings)}
        cache.set(cache_key, all_embeddings, 60 * 60)
    return all_embeddings

def get_recommendations(user):
    all_embeddings = get_all_video_embeddings()
    if not all_embeddings:
        return Video.objects.none()

    video_ids, embeddings_matrix = zip(*all_embeddings.items())
    embeddings_matrix = np.array(embeddings_matrix)

    recent_views = UserInteraction.objects.filter(user=user, interaction_type='view').order_by('-timestamp')[:10]
    watched_video_ids = {view.video_id for view in recent_views}

    if not watched_video_ids:
        return Video.objects.all().order_by('-uploaded_at')[:20]

    watched_embeddings = [all_embeddings[vid] for vid in watched_video_ids if vid in all_embeddings]
    if not watched_embeddings:
         return Video.objects.all().order_by('-uploaded_at')[:20]

    user_interest_vector = np.mean(watched_embeddings, axis=0).reshape(1, -1)
    similarities = cosine_similarity(user_interest_vector, embeddings_matrix)[0]
    sorted_indices = np.argsort(similarities)[::-1]
    recommended_ids = [video_ids[i] for i in sorted_indices if video_ids[i] not in watched_video_ids]

    if not recommended_ids:
        return Video.objects.exclude(id__in=watched_video_ids).order_by('-uploaded_at')[:20]

    recommended_videos = list(Video.objects.filter(id__in=recommended_ids[:20]))
    recommended_videos.sort(key=lambda x: recommended_ids.index(x.id))
    return recommended_videos
