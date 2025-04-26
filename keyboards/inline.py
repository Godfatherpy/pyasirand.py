# keyboards/inline.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def video_navigation_keyboard():
    """
    Returns an inline keyboard with Previous, Next, and Category buttons.
    """
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

def category_keyboard(categories):
    """
    Returns an inline keyboard for category selection.
    :param categories: List of category dicts, each with a 'name' field.
    """
    keyboard = [
        [InlineKeyboardButton(cat['name'], callback_data=f"category_{cat['name']}")]
        for cat in categories
    ]
    return InlineKeyboardMarkup(keyboard)
