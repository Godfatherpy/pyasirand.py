# bot.py
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Config
from config import TELEGRAM_BOT_TOKEN, MONGODB_URI

# Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Bot started!")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("✅ Action processed")

# Core Application
async def init_db(application):
    """Initialize database connection"""
    from pymongo import MongoClient
    application.bot_data["db"] = MongoClient(MONGODB_URI).get_database()
    logging.info("Database initialized")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"🚨 Error: {context.error}", exc_info=True)

async def run_bot():
    """Separate coroutine for bot execution"""
    application = None
    try:
        application = (
            ApplicationBuilder()
            .token(TELEGRAM_BOT_TOKEN)
            .post_init(init_db)
            .build()
        )

        # Register handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(handle_buttons))
        application.add_error_handler(error_handler)

        logging.info("🤖 Starting bot in polling mode...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        
        # Keep running until manually stopped
        while True:
            await asyncio.sleep(3600)  # Sleep 1 hour between checks
            
    except asyncio.CancelledError:
        logging.info("🛑 Graceful shutdown requested")
    except Exception as e:
        logging.critical(f"💥 Fatal error: {e}", exc_info=True)
    finally:
        if application:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
        logging.info("🧹 Cleanup completed")

def main():
    """Main entry point with proper event loop handling"""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        logging.info("👋 Bot stopped by user")
    except Exception as e:
        logging.critical(f"❌ Unhandled exception: {e}", exc_info=True)
    finally:
        logging.info("🔚 Process terminated")
        if loop.is_running():
            loop.close()

if __name__ == "__main__":
    main()
