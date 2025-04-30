import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

# Optional: Admin user IDs (comma-separated in .env or environment variables)
admin_ids_env = os.getenv("ADMIN_IDS", "1920026281")
try:
    ADMIN_IDS = [int(uid.strip()) for uid in admin_ids_env.split(",") if uid.strip()]
except ValueError as e:
    raise ValueError(f"Invalid ADMIN_IDS in environment: {admin_ids_env}") from e

# Optional: Default settings
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")
try:
    VIDEO_LIMIT_PER_DAY = int(os.getenv("VIDEO_LIMIT_PER_DAY", "20"))
except ValueError:
    VIDEO_LIMIT_PER_DAY = 20

if not TELEGRAM_BOT_TOKEN or not MONGODB_URI:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN and MONGODB_URI must be set in environment variables or .env file"
    )

URL_SHORTENER_API = os.getenv(
    "URL_SHORTENER_API",
    "https://easysky.in/st?api=c140f4465e38cdee50c2694418c299a3ca5b25db&url=yourdestinationlink.com"
)
