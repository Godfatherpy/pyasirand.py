# handlers/admin.py

from telegram import Update
from telegram.ext import ContextTypes
from db.models import add_category, remove_category, get_category
from config import ADMIN_IDS

# --- Helper: Check if user is admin ---
def is_admin(user_id):
    return user_id in ADMIN_IDS

# --- /addcategory command ---
async def add_category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /addcategory <category_name> <channel_id>")
        return

    category_name = args[0]
    channel_id = args[1]
    db = context.bot_data['db_client']

    if get_category(db, category_name):
        await update.message.reply_text(f"Category '{category_name}' already exists.")
        return

    add_category(db, category_name, channel_id)
    await update.message.reply_text(f"✅ Category '{category_name}' added with channel ID {channel_id}.")

# --- /removecategory command ---
async def remove_category_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /removecategory <category_name>")
        return

    category_name = args[0]
    db = context.bot_data['db_client']

    if not get_category(db, category_name):
        await update.message.reply_text(f"Category '{category_name}' does not exist.")
        return

    remove_category(db, category_name)
    await update.message.reply_text(f"✅ Category '{category_name}' removed.")

# --- Admin callback (for future admin inline actions) ---
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if not is_admin(user_id):
        await query.answer("You are not authorized.", show_alert=True)
        return

    # Example: handle admin inline actions here
    await query.answer("Admin action performed.")
  
