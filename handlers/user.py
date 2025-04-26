# handlers/user.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.utils import get_or_create_user, get_category_list
from db.models import (
    get_unseen_video, add_video_to_history, update_user_category
)
from config import ADMIN_IDS

# --- /start command ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db_client']
    user = get_or_create_user(db, user_id)
    await update.message.reply_text(
        "👋 Welcome! Use /getvideo or the button below to get a random video.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 Get Video", callback_data="getvideo")]
        ])
    )

# --- /getvideo command or button ---
async def get_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data['db_client']
    user = get_or_create_user(db, user_id)
    category = user.get("selected_category") or "general"
    video = get_unseen_video(db, user_id, category)
    if not video:
        await update.message.reply_text("No more unseen videos in this category! Try another category.")
        return

    # Send the video
    await update.message.reply_video(
        video=video["file_id"],
        caption=f"Category: {category}",
        reply_markup=video_navigation_keyboard(category)
    )
    # Add to user history
    add_video_to_history(db, user_id, str(video["_id"]))

# --- Navigation callback (Next/Previous) ---
async def navigation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    db = context.bot_data['db_client']
    user = get_or_create_user(db, user_id)
    category = user.get("selected_category") or "general"
    video = get_unseen_video(db, user_id, category)
    if not video:
        await query.edit_message_caption("No more unseen videos in this category!")
        return
    await query.edit_message_media(
        media=video["file_id"],
        reply_markup=video_navigation_keyboard(category)
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

# --- Helper: Inline keyboard for navigation and category ---
def video_navigation_keyboard(current_category):
    categories = get_category_list  # This should be a function call, but for inline keyboards, you may want to cache or pass categories.
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
