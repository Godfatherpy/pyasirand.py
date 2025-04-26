# db/utils.py

from pymongo import MongoClient
from config import MONGODB_URI
from datetime import datetime

# --- MongoDB Initialization ---

def init_db(uri=MONGODB_URI, db_name="telegram_video_bot"):
    """
    Initialize and return a MongoDB database instance.
    
    Args:
        uri (str): MongoDB connection URI.
        db_name (str): Name of the database to use.
        
    Returns:
        Database: pymongo Database instance.
    """
    client = MongoClient(uri)
    db = client[db_name]
    return db

# --- Utility Functions ---

def get_or_create_user(db, user_id):
    """
    Retrieve a user document by user_id or create a new one if not found.
    
    Args:
        db (Database): MongoDB database instance.
        user_id (int): Telegram user ID.
        
    Returns:
        dict: User document.
    """
    user = db.users.find_one({"user_id": user_id})
    if user is None:
        user = {
            "user_id": user_id,
            "is_premium": False,
            "history": [],
            "selected_category": None,
            "tokens": 0,
            "limits": {
                "daily": 0,
                "last_reset": None
            }
        }
        db.users.insert_one(user)
    return user

def get_category_list(db):
    """
    Retrieve a list of all categories with their name and channel_id.
    
    Args:
        db (Database): MongoDB database instance.
        
    Returns:
        list: List of category documents.
    """
    categories = db.categories.find({}, {"_id": 0, "name": 1, "channel_id": 1})
    return list(categories)

def is_user_admin(user_id, admin_ids):
    """
    Check if a user ID is in the list of admin IDs.
    
    Args:
        user_id (int): Telegram user ID.
        admin_ids (list): List of admin user IDs.
        
    Returns:
        bool: True if user is admin, False otherwise.
    """
    return user_id in admin_ids

def reset_user_limits(db, user_id):
    """
    Reset the daily usage limits for a user.
    
    Args:
        db (Database): MongoDB database instance.
        user_id (int): Telegram user ID.
    """
    db.users.update_one(
        {"user_id": user_id},
        {"$set": {"limits.daily": 0, "limits.last_reset": datetime.utcnow()}}
    )
    
