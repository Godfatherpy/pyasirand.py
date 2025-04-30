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

# Health Check Server
async def health_server():
    """Dummy TCP server for health checks"""
    async def handle(_reader, _writer):
        _writer.close()
        await _writer.wait_closed()

    server = await asyncio.start_server(handle, '0.0.0.0', 8000)
    async with server:
        await server.serve_forever()

# Bot Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Bot is operational!")

async def run_bot():
    # Start health check server
    health_task = asyncio.create_task(health_server())
    
    # Initialize bot
    application = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )
    
    application.add_handler(CommandHandler("start", start_command))
    
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # Keep both services running
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
