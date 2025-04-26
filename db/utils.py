# db/utils.py

from pymongo import MongoClient
from config import MONGODB_URI

# --- MongoDB Initialization ---
def init_db(uri=MONGODB_URI, db_name="telegram_video_bot"):
    """
    Initializes and returns a MongoDB database instance.
    """
    client = MongoClient(uri)
    db = client[db_name]
    return db

# --- Utility Functions ---

def get_or_create_user(db, user_id):
    """
    Retrieves a user document or creates it if not found.
    """
    user = db.users.find_one({"user_id": user_id})
    if user is None:
        user = {
            "user_id": user_id,
            "is_premium": False,
            "history": [],
            "selected_category": None,
            "tokens": 0,
            "limits": {"daily": 0, "last_reset": None}
        }
        db.users.insert_one(user)
    return user

def get_category_list(db):
    """
    Returns a list of all categories.
    """
    return list(db.categories.find({}, {"_id": 0, "name": 1, "channel_id": 1}))

def is_user_admin(user_id, admin_ids):
    """
    Checks if the user is an admin.
    """
    return user_id in admin_ids

def reset_user_limits(db, user_id):
    """
    Resets the user's daily limits.
    """
    from datetime import datetime
    db.users.update_one(
        {"user_id": user_id},
        {"$set": {"limits.daily": 0, "limits.last_reset": datetime.utcnow()}}
    )


