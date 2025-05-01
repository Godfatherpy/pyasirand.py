import logging
import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from config import TELEGRAM_BOT_TOKEN, MONGODB_URI
from pymongo import MongoClient

# --- Import your handlers ---
from handlers.user import (
    start_command,
    get_video_command,
    navigation_callback,
    category_callback,
    show_categories_callback,
)
from handlers.admin import (
    add_category_command,
    remove_category_command,
    admin_callback,
)

# --- Health Check Server ---
async def health_server():
    async def handle(_reader, _writer):
        _writer.close()
        await _writer.wait_closed()
    server = await asyncio.start_server(handle, '0.0.0.0', 8000)
    async with server:
        await server.serve_forever()

# --- DB Initialization ---
async def init_db(application):
    try:
        client = MongoClient(MONGODB_URI)
        db_name = client.get_database().name
        if not db_name or db_name == 'test':
            db = client['telegram_video_bot']
        else:
            db = client.get_database()
        application.bot_data['db_client'] = db
        logging.info(f"✅ MongoDB connected to database: {db.name}")
    except Exception as e:
        logging.error(f"❌ MongoDB connection error: {e}")
        raise

# --- Main Bot Runner ---
async def run_bot():
    # Start health check server
    health_task = asyncio.create_task(health_server())

    # Initialize bot
    application = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # --- Initialize DB before adding handlers ---
    await init_db(application)

    # --- Register User Commands ---
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("getvideo", get_video_command))

    # --- Register Admin Commands ---
    application.add_handler(CommandHandler("addcategory", add_category_command))
    application.add_handler(CommandHandler("removecategory", remove_category_command))

    # --- Register Callback Handlers ---
    application.add_handler(CallbackQueryHandler(navigation_callback, pattern="^(prev_|next_).*"))
    application.add_handler(CallbackQueryHandler(category_callback, pattern="^category_"))
    application.add_handler(CallbackQueryHandler(show_categories_callback, pattern="^show_categories$"))
    application.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))

    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        while True:
            await asyncio.sleep(3600)
    finally:
        health_task.cancel()
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        logging.info("👋 Graceful shutdown")
    finally:
        if loop.is_running():
            loop.stop()
        if not loop.is_closed():
            loop.close()

if __name__ == "__main__":
    main()
