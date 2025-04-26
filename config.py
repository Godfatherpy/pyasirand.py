
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("7646433933:AAFNt3yLxXuwOPhJEfGyFtvNgkljQgJx-Wk")
MONGODB_URI = os.getenv("mongodb+srv://babuhaiker:<pOstGjwAZDVYDSNK>@cluster0.hycmfqe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Optional: Admin user IDs (comma-separated in .env)
ADMIN_IDS = [int(uid) for uid in os.getenv("1920026281", "").split(",") if uid.strip()]

# Optional: Default settings
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")
VIDEO_LIMIT_PER_DAY = int(os.getenv("VIDEO_LIMIT_PER_DAY", "20"))

if not TELEGRAM_BOT_TOKEN or not MONGODB_URI:
    raise ValueError("TELEGRAM_BOT_TOKEN and MONGODB_URI must be set in environment variables or .env file")
  
# config.py

URL_SHORTENER_API = "https://easysky.in/st?api=c140f4465e38cdee50c2694418c299a3ca5b25db&url=yourdestinationlink.com"
