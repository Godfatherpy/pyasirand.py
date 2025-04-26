
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# --- Database Initialization (used by init_db in utils.py) ---
def get_db(client: MongoClient, db_name="telegram_video_bot"):
    return client[db_name]

# --- User Management ---
def get_user(db, user_id):
    return db.users.find_one({"user_id": user_id})

def create_user(db, user_id, is_premium=False):
    user = {
        "user_id": user_id,
        "is_premium": is_premium,
        "history": [],  # List of video_ids seen
        "selected_category": None,
        "tokens": 0,
        "limits": {"daily": 0, "last_reset": datetime.utcnow()}
    }
    db.users.insert_one(user)
    return user

def update_user_category(db, user_id, category):
    db.users.update_one({"user_id": user_id}, {"$set": {"selected_category": category}})

def add_video_to_history(db, user_id, video_id):
    db.users.update_one({"user_id": user_id}, {"$addToSet": {"history": video_id}})

def reset_daily_limits(db, user_id):
    db.users.update_one(
        {"user_id": user_id},
        {"$set": {"limits.daily": 0, "limits.last_reset": datetime.utcnow()}}
    )

# --- Category Management ---
def get_categories(db):
    return list(db.categories.find({}))

def get_category(db, category_name):
    return db.categories.find_one({"name": category_name})

def add_category(db, name, channel_id):
    db.categories.insert_one({"name": name, "channel_id": channel_id})

def remove_category(db, name):
    db.categories.delete_one({"name": name})

# --- Video History (per user, per category) ---
def get_unseen_video(db, user_id, category):
    user = get_user(db, user_id)
    seen_videos = user.get("history", [])
    # Find a random unseen video in the category's channel
    video = db.videos.find_one({
        "category": category,
        "_id": {"$nin": [ObjectId(vid) for vid in seen_videos]}
    })
    return video

def add_video(db, video_id, category, file_id):
    db.videos.insert_one({
        "_id": video_id,
        "category": category,
        "file_id": file_id
    })

# --- Admin Management (if needed) ---
def is_admin(user_id, admin_ids):
    return user_id in admin_ids


