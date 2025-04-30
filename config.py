import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Required Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

# Admin Configuration
ADMIN_IDS = []
try:
    admin_ids_env = os.getenv("ADMIN_IDS", "1920026281")
    ADMIN_IDS = [int(uid.strip()) for uid in admin_ids_env.split(",") if uid.strip()]
except ValueError as e:
    raise ValueError(f"Invalid ADMIN_IDS format. Use comma-separated numbers. Error: {e}")

# User Limits
try:
    VIDEO_LIMIT_PER_DAY = int(os.getenv("VIDEO_LIMIT_PER_DAY", "20"))
except ValueError:
    VIDEO_LIMIT_PER_DAY = 20
    print(f"⚠️ Using default VIDEO_LIMIT_PER_DAY: {VIDEO_LIMIT_PER_DAY}")

# Default Settings
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")
URL_SHORTENER_API = os.getenv(
    "URL_SHORTENER_API",
    "https://easysky.in/st?api=c140f4465e38cdee50c2694418c299a3ca5b25db&url=yourdestinationlink.com"
)

# Validation
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN missing in .env/environment")
if not MONGODB_URI:
    raise ValueError("❌ MONGODB_URI missing in .env/environment")
if not ADMIN_IDS:
    print("⚠️ No admin IDs specified - some admin commands will be disabled")

# Optional Debugging
if os.getenv("DEBUG_MODE", "false").lower() == "true":
    print("🔧 Debug mode activated")
