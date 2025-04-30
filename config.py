import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")
URL_SHORTENER_API = os.getenv("URL_SHORTENER_API")

if not TELEGRAM_BOT_TOKEN or not MONGODB_URI or not URL_SHORTENER_API:
    raise ValueError("Missing required environment variables")
