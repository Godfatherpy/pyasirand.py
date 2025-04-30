import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")
URL_SHORTENER_API = os.getenv("URL_SHORTENER_API")
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")
VIDEO_LIMIT_PER_DAY = int(os.getenv("VIDEO_LIMIT_PER_DAY", 20))

# Parse ADMIN_IDS as a list of integers from comma-separated string
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

if not TELEGRAM_BOT_TOKEN or not MONGODB_URI or not URL_SHORTENER_API:
    raise ValueError("Missing required environment variables")
