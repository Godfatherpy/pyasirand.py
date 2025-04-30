import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import TELEGRAM_BOT_TOKEN, MONGODB_URI
from handlers.user import (
    start_command,
    get_video_command,
    navigation_callback,
    category_callback,
)
from handlers.admin import (
    add_category_command,
    remove_category_command,
    admin_callback,
)
from db import init_db

# --- Logging Setup ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def init_db_client(application):
    """Proper async initialization"""
    application.bot_data["db_client"] = init_db(MONGODB_URI)
    logger.info("Database initialized")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global error handler"""
    logger.error(f"Error: {context.error}", exc_info=True)

async def main():
    """Main async entry point"""
    application = None
    try:
        application = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .post_init(init_db_client)
            .build()
        )

        # --- Handler Registration ---
        handlers = [
            CommandHandler("start", start_command),
            CommandHandler("getvideo", get_video_command),
            CallbackQueryHandler(navigation_callback, pattern=r"^(next|prev)_"),
            CallbackQueryHandler(category_callback, pattern=r"^category_"),
            CommandHandler("addcategory", add_category_command),
            CommandHandler("removecategory",
