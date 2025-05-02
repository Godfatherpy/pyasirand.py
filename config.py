import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    MONGO_URI = os.getenv("MONGODB_URI")
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS").split(",")]
    DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")
    INITIAL_TOKENS = int(os.getenv("INITIAL_TOKENS", 5))
    TOKEN_EXPIRY_HOURS = int(os.getenv("TOKEN_EXPIRY_HOURS", 24))
    URL_SHORTENER = os.getenv("URL_SHORTENER_API")
    DB_NAME = "spicybot"