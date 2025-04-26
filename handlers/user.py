# handlers/user.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from db.utils import get_or_create_user, get_category_list
from db.models import (
    update_user_category, add_video_to_history
)
from services.video_service import fetch_random_video
from services.url_shortener import generate_24h_token_url
from config import ADMIN_IDS
from datetime import datetime

# --- /start command ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db_client']
    user = get_or_create_user(db, user_id)

    # Check token expiry (assume user['token_expiry'] exists, or set it)
    now = int(datetime.utcnow().timestamp())
    token_expiry = user.get("token_expiry", 0)

    if user_id not in ADMIN_IDS and now > token_expiry:
        # Generate new 24-hour token link
        short_url, expiry = generate_24h_token_url(context.bot.username, user_id)
        db.users.update_one({"user_id": user_id}, {"$set": {"token_expiry": expiry}})
        await update.message.reply_text(
            f"🕒 Your access token expired!\n\n"
            f"Click the link below to refresh your access for 24 hours:\n\n"
            f"{short_url}\n\n"
            f"After opening the link, come back and use the bot again."
        )
        return

    await update.message.reply_text(
        "👋 Welcome! Use /getvideo or the button below to get a random video.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Get Video", callback_data="getvideo")],
            [InlineKeyboardButton("📂 Choose Category", callback_data="show_categories")]
        ])
    )

# --- /getvideo command or button ---
async def get_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db_client']
    user = get_or_create_user(db, user_id)

    # Check token expiry for non-admins
    now = int(datetime.utcnow().timestamp())
    token_expiry = user.get("token_expiry", 0)
    if user_id not in ADMIN_IDS and now > token_expiry:
        short_url, expiry = generate_24h_token_url(context.bot.username, user_id)
        db.users.update_one({"user_id": user_id}, {"$set": {"token_expiry": expiry}})
        await update.message.reply_text(
            f"🕒 Your access token expired!\n\n"
            f"Click the link below to refresh your access for 24 hours:\n\n"
            f"{short_url}\n\n"
            f"After opening the link, come back and use the bot again."
        )
        return

    category = user.get("selected_category") or "general"
    video = fetch_random_video(db, user_id, category)
    if not video:
        await update.message.reply_text("No more unseen videos in this category! Try another category.")
        return

    await update.message.reply_video(
        video=video["file_id"],
        caption=f"Category: {category}",
        reply_markup=video_navigation_keyboard()
    )
    add_video_to_history(db, user_id, str(video["_id"]))

# --- Navigation callback (Next/Previous) ---
async def navigation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    db = context.bot_data['db_client']
    user = get_or_create_user(db, user_id)

    # Token expiry check
    now = int(datetime.utcnow().timestamp())
    token_expiry = user.get("token_expiry", 0)
    if user_id not in ADMIN_IDS and now > token_expiry:
        short_url, expiry = generate_24h_token_url(context.bot.username, user_id)
        db.users.update_one({"user_id": user_id}, {"$set": {"token_expiry": expiry}})
        await query.edit_message_text(
            f"🕒 Your access token expired!\n\n"
            f"Click the link below to refresh your access for 24 hours:\n\n"
            f"{short_url}\n\n"
            f"After opening the link, come back and use the bot again."
        )
        return

    category = user.get("selected_category") or "general"
    video = fetch_random_video(db, user_id, category)
    if not video:
        await query.edit_message_caption("No more unseen videos in this category!")
        return

    await query.edit_message_media(
        media=video["file_id"],
        reply_markup=video_navigation_keyboard()
    )
    add_video_to_history(db, user_id, str(video["_id"]))

# --- Category selection callback ---
async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    db = context.bot_data['db_client']
    user_id = query.from_user.id
    category_name = query.data.replace("category_", "")
    update_user_category(db, user_id, category_name)
    await query.edit_message_text(f"✅ Category switched to: {category_name}\nUse /getvideo to get a video.")

# --- Show categories (triggered by "Category" button) ---
async def show_categories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    db = context.bot_data['db_client']
    categories = get_category_list(db)
    keyboard = [
        [InlineKeyboardButton(cat['name'], callback_data=f"category_{cat['name']}")]
        for cat in categories
    ]
    await query.edit_message_text(
        "Select a category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Helper: Inline keyboard for navigation ---
def video_navigation_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Previous", callback_data="prev_"),
            InlineKeyboardButton("➡️ Next", callback_data="next_"),
        ],
        [
            InlineKeyboardButton("📂 Category", callback_data="show_categories")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Register these handlers in your bot.py ---
# CommandHandler("start", start_command)
# CommandHandler("getvideo", get_video_command)
# CallbackQueryHandler(navigation_callback, pattern="^(next_|prev_)")
# CallbackQueryHandler(category_callback, pattern="^category_")
# CallbackQueryHandler(show_categories_callback, pattern="^show_categories$")

