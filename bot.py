# bot.py

import logging
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from telegram import Update

from config import TELEGRAM_BOT_TOKEN, MONGODB_URI
from handlers.user import (
    start_command, get_video_command, navigation_callback, category_callback
)
from handlers.admin import (
    add_category_command, remove_category_command, admin_callback
)
from db import init_db

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Main Bot Setup ---
async def main():
    # Initialize MongoDB
    db_client = init_db(MONGODB_URI)
    
    # Create the bot application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Pass db_client to handlers via context
    application.bot_data['db_client'] = db_client

    # --- User Commands ---
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('getvideo', get_video_command))
    application.add_handler(CallbackQueryHandler(navigation_callback, pattern='^(next|prev)_'))
    application.add_handler(CallbackQueryHandler(category_callback, pattern='^category_'))

    # --- Admin Commands ---
    application.add_handler(CommandHandler('addcategory', add_category_command))
    application.add_handler(CommandHandler('removecategory', remove_category_command))
    application.add_handler(CallbackQueryHandler(admin_callback, pattern='^admin_'))

    # --- Run Bot ---
    logger.info("Bot started!")
    await application.run_polling()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
  
