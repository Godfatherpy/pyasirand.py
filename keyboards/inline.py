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

    :param categories: List of category dicts, each with a 'name' key.
    """
    if not isinstance(categories, list):
        raise ValueError("categories must be a list of dicts with a 'name' key")

    keyboard = []
    for cat in categories:
        name = cat.get('name')
        if not name:
            continue  # skip if no name
        keyboard.append([InlineKeyboardButton(name, callback_data=f"category_{name}")])

    if not keyboard:
        # Fallback button if no categories
        keyboard = [[InlineKeyboardButton("No categories found", callback_data="none")]]

    return InlineKeyboardMarkup(keyboard)
