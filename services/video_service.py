
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
    # Convert only valid ObjectId strings
    seen_object_ids = []
    for vid in seen_video_ids:
        try:
            seen_object_ids.append(ObjectId(vid))
        except Exception:
            continue

    unseen_videos = list(db.videos.find({
        "category": category,
        "_id": {"$nin": seen_object_ids}
    }))

    if not unseen_videos:
        return None

    return random.choice(unseen_videos)

def mark_video_as_seen(db, user_id, video_id):
    """
    Add the video_id to the user's history.
    """
    # Accept both ObjectId and str for video_id
    video_id_str = str(video_id)
    db.users.update_one(
        {"user_id": user_id},
        {"$addToSet": {"history": video_id_str}}
    )

def get_video_history(db, user_id, limit=20):
    """
    Retrieve the most recent video IDs watched by the user.
    """
    user = db.users.find_one({"user_id": user_id})
    if not user:
        return []
    # Ensure history is a list
    history = user.get("history", [])
    if not isinstance(history, list):
        history = []
    return history[-limit:]
