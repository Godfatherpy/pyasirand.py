# services/video_service.py

import random
from bson.objectid import ObjectId

def fetch_random_video(db, user_id, category):
    """
    Fetch a random, unseen video for the user from the specified category.
    Returns None if no unseen videos are available.
    """
    user = db.users.find_one({"user_id": user_id})
    if not user:
        return None

    seen_video_ids = user.get("history", [])
    # Get all unseen videos in the category
    unseen_videos = list(db.videos.find({
        "category": category,
        "_id": {"$nin": [ObjectId(vid) for vid in seen_video_ids]}
    }))

    if not unseen_videos:
        return None

    # Pick one at random
    video = random.choice(unseen_videos)
    return video

def mark_video_as_seen(db, user_id, video_id):
    """
    Add the video_id to the user's history.
    """
    db.users.update_one(
        {"user_id": user_id},
        {"$addToSet": {"history": str(video_id)}}
    )

def get_video_history(db, user_id, limit=20):
    """
    Retrieve the most recent video IDs watched by the user.
    """
    user = db.users.find_one({"user_id": user_id})
    if not user:
        return []
    return user.get("history", [])[-limit:]
  
