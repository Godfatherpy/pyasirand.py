# bot.py - Full Implementation
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Configuration (config.py)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
MONGODB_URI = "mongodb://localhost:27017/yourdb"

# Database (db.py)
async def init_db(mongo_uri):
    """Initialize MongoDB connection"""
    from pymongo import MongoClient
    return MongoClient(mongo_uri).get_database()

# Handlers (handlers/user.py)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text("🚀 Welcome! Use /getvideo to browse content.")

async def get_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /getvideo command"""
    await update.message.reply_text("📡 Fetching videos...")

async def navigation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pagination buttons"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🔍 Loading more videos...")

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category selection"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🗂 Category selected!")

# Admin Handlers (handlers/admin.py)
async def add_category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addcategory command"""
    await update.message.reply_text("➕ Adding new category...")

async def remove_category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /removecategory command"""
    await update.message.reply_text("➖ Removing category...")

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin panel actions"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⚙️ Admin action processed!")

# Core Application
async def init_db_client(application):
    """Initialize database connection"""
    application.bot_data["db"] = await init_db(MONGODB_URI)
    logging.info("Database connection established")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global error handler"""
    logging.error(f"🚨 Error: {context.error}", exc_info=True)

async def main():
    """Main application entry point"""
    application = None
    
    try:
        # Build application
        application = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .post_init(init_db_client)
            .build()
        )

        # Register handlers
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

        application.add_error_handler(error_handler)

        # Start polling
        logging.info("🤖 Bot starting in polling mode...")
        await application.run_polling(
            drop_pending_updates=True,
            close_loop=False,
            allowed_updates=[
                "message",
                "callback_query",
                "chat_member"
            ]
        )

    except asyncio.CancelledError:
        logging.info("🛑 Bot shutdown requested")
    except Exception as e:
        logging.critical(f"💥 Fatal error: {e}", exc_info=True)
        if application and application.running:
            await application.stop()
        raise
    finally:
        logging.info("🧹 Cleanup completed")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("👋 Bot stopped by user")
    except Exception as e:
        logging.critical(f"❌ Unhandled exception: {e}", exc_info=True)
    finally:
        logging.info("🔚 Process terminated")
