
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

# Optional: Admin user IDs (comma-separated in .env)
ADMIN_IDS = [int(uid) for uid in os.getenv("ADMIN_IDS", "").split(",") if uid.strip()]

# Optional: Default settings
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")
VIDEO_LIMIT_PER_DAY = int(os.getenv("VIDEO_LIMIT_PER_DAY", "20"))

if not TELEGRAM_BOT_TOKEN or not MONGODB_URI:
    raise ValueError("TELEGRAM_BOT_TOKEN and MONGODB_URI must be set in environment variables or .env file")
  
