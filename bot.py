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

async def store_db_client(db_client):
    """Custom post_init handler to store database client"""
    async def callback(application):
        application.bot_data["db_client"] = db_client
        logger.info("Database client stored in bot_data")
    return callback

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global error handler"""
    logger.error(f"Update {update} caused error: {context.error}", exc_info=True)

async def main():
    # Initialize MongoDB client
    db_client = init_db(MONGODB_URI)
    
    try:
        application = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .post_init(store_db_client(db_client))
            .build()
        )

        # --- Handler Registration ---
        handlers = [
            CommandHandler("start", start_command),
            CommandHandler("getvideo", get_video_command),
            CallbackQueryHandler(navigation_callback, pattern=r"^(next|prev)_"),
            CallbackQueryHandler(category_callback, pattern=r"^category_"),
            CommandHandler("addcategory", add_category_command),
            CommandHandler("removecategory", remove_category_command),
            CallbackQueryHandler(admin_callback, pattern=r"^admin_"),
        ]
        
        for handler in handlers:
            application.add_handler(handler)

        # Add error handler
        application.add_error_handler(error_handler)

        # --- Start Polling ---
        logger.info("Bot started with production configuration")
        await application.run_polling(
            drop_pending_updates=True,
            close_loop=False,
            stop_signals=None,
            allowed_updates=[
                "message",
                "callback_query",
                "chat_member",
                "my_chat_member"
            ]
        )

    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
    finally:
        logger.info("Bot process terminated")
