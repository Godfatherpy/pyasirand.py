from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from config import Config
from database import Database
from keyboards import main_keyboard, expired_keyboard
from services.url_shortener import generate_24h_token_url

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = Database.get_user(user_id)
    
    if not user:
        new_user = {
            "user_id": user_id,
            "tokens": Config.INITIAL_TOKENS,
            "token_expiry": (datetime.now() + timedelta(hours=Config.TOKEN_EXPIRY_HOURS)).isoformat(),
            "subscription": False,
            "cursor": 0,
            "current_category": Config.DEFAULT_CATEGORY,
            "viewed_videos": []
        }
        Database.update_user(user_id, new_user)
        await update.message.reply_text(
            f"🎥 Welcome! You've received {Config.INITIAL_TOKENS} free tokens "
            f"(valid for {Config.TOKEN_EXPIRY_HOURS} hours)"
        )
    else:
        remaining_time = datetime.fromisoformat(user['token_expiry']) - datetime.now()
        hours = max(0, int(remaining_time.total_seconds() // 3600))
        await update.message.reply_text(
            f"👋 Welcome back! Tokens: {user.get('tokens', 0)} "
            f"(expires in {hours} hours)"
        )
    
    await send_current_video(update, context)

async def send_current_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = Database.get_user(user_id)
    
    if not check_access(user):
        short_url, expiry = generate_24h_token_url(context.bot.username, user_id)
        Database.update_user(user_id, {"token_expiry": expiry.isoformat()})
        await update.message.reply_text(
            f"🕒 Your access token expired!\n\n"
            f"Click the link below to refresh your access for 24 hours:\n\n"
            f"{short_url}\n\n"
            f"After opening the link, come back and use the bot again.",
            reply_markup=expired_keyboard()
        )
        return

    videos = Database.get_videos(user['current_category'], user['cursor'])
    
    if videos:
        await update.message.reply_video(
            video=videos[0]['file_id'],
            caption=f"Category: {user['current_category']}",
            reply_markup=main_keyboard(user['current_category'])
        )
        # Mark video as viewed
        Database.update_user(user_id, {
            "$push": {"viewed_videos": videos[0]['file_id']},
            "$inc": {"tokens": -1}
        })
    else:
        await update.message.reply_text(
            "No videos available in this category.",
            reply_markup=main_keyboard()
        )

async def navigation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = Database.get_user(user_id)
    
    if not check_access(user):
        short_url, expiry = generate_24h_token_url(context.bot.username, user_id)
        Database.update_user(user_id, {"token_expiry": expiry.isoformat()})
        await query.edit_message_text(
            f"🕒 Your access token expired!\n\n"
            f"Click the link below to refresh your access for 24 hours:\n\n"
            f"{short_url}\n\n"
            f"After opening the link, come back and use the bot again.",
            reply_markup=expired_keyboard()
        )
        return

    action = query.data
    new_category = None
    
    if action == 'next':
        user['cursor'] += 1
    elif action == 'prev':
        user['cursor'] = max(0, user['cursor'] - 1)
    elif action.startswith('cat_'):
        new_category = action.split('_')[1]
        user['current_category'] = new_category
        user['cursor'] = 0

    Database.update_user(user_id, user)
    await update_video_display(query, user_id)

async def update_video_display(query, user_id):
    user = Database.get_user(user_id)
    videos = Database.get_videos(user['current_category'], user['cursor'])
    
    if videos:
        await query.edit_message_media(
            InputMediaVideo(
                videos[0]['file_id'],
                caption=f"Category: {user['current_category']}"
            ),
            reply_markup=main_keyboard(user['current_category'])
        )
        # Mark video as viewed
        Database.update_user(user_id, {
            "$push": {"viewed_videos": videos[0]['file_id']},
            "$inc": {"tokens": -1}
        })
    else:
        await query.edit_message_text(
            "End of list 🏁",
            reply_markup=main_keyboard()
        )

async def show_categories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    categories = Database.get_categories()
    keyboard = [
        [InlineKeyboardButton(cat['name'], callback_data=f"cat_{cat['name']}")]
        for cat in categories
    ]
    await query.edit_message_text(
        "Select a category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def check_access(user):
    if user.get('subscription'):
        return True
    if user.get('tokens', 0) > 0 and datetime.fromisoformat(user['token_expiry']) > datetime.now():
        return True
    return False