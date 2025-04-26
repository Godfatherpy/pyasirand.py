# utils/decorators.py

from functools import wraps
from config import ADMIN_IDS

def admin_only(handler_func):
    """
    Decorator to restrict a command to admins only.
    """
    @wraps(handler_func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            if update.message:
                await update.message.reply_text("❌ You are not authorized to use this command.")
            elif update.callback_query:
                await update.callback_query.answer("❌ You are not authorized.", show_alert=True)
            return
        return await handler_func(update, context, *args, **kwargs)
    return wrapper

def premium_required(handler_func):
    """
    Decorator to restrict a command to premium users only.
    Assumes 'is_premium' is stored in the user's DB document.
    """
    @wraps(handler_func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        db = context.bot_data['db_client']
        user = db.users.find_one({"user_id": user_id})
        if not user or not user.get("is_premium", False):
            if update.message:
                await update.message.reply_text("🔒 This feature is for premium users only.")
            elif update.callback_query:
                await update.callback_query.answer("🔒 Premium only.", show_alert=True)
            return
        return await handler_func(update, context, *args, **kwargs)
    return wrapper
