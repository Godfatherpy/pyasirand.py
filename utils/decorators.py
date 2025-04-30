from functools import wraps
from config import ADMIN_IDS

def admin_only(handler_func):
    """
    Decorator to restrict a command to admins only.
    """
    @wraps(handler_func)
    async def wrapper(update, context, *args, **kwargs):
        user = getattr(update, "effective_user", None)
        user_id = getattr(user, "id", None)
        if user_id not in ADMIN_IDS:
            # Handle both message and callback_query cases
            if hasattr(update, "message") and update.message:
                await update.message.reply_text("❌ You are not authorized to use this command.")
            elif hasattr(update, "callback_query") and update.callback_query:
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
        user = getattr(update, "effective_user", None)
        user_id = getattr(user, "id", None)
        db = context.bot_data.get('db_client')
        user_doc = None
        if db:
            user_doc = db.users.find_one({"user_id": user_id})
        if not user_doc or not user_doc.get("is_premium", False):
            if hasattr(update, "message") and update.message:
                await update.message.reply_text("🔒 This feature is for premium users only.")
            elif hasattr(update, "callback_query") and update.callback_query:
                await update.callback_query.answer("🔒 Premium only.", show_alert=True)
            return
        return await handler_func(update, context, *args, **kwargs)
    return wrapper
