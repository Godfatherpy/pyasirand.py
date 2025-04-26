# services/url_shortener.py

import requests
from helper import str_to_b64, get_current_time
from config import URL_SHORTENER_API

def shorten_url(long_url):
    """
    Shortens a URL using the configured shortener service.
    """
    api_url = URL_SHORTENER_API.format(long_url)
    try:
        response = requests.get(api_url, timeout=10)
        # Many services return the short link as plain text, some as JSON.
        # Try to extract the link accordingly:
        if response.status_code == 200:
            # If the response is a JSON with a 'shortenedUrl' or similar key:
            try:
                data = response.json()
                # Try common keys, adjust as needed:
                for key in ['shortenedUrl', 'short_url', 'shortened', 'url']:
                    if key in data:
                        return data[key]
            except Exception:
                # If not JSON, fallback to plain text
                return response.text.strip()
        return long_url  # fallback to original if failed
    except Exception as e:
        print(f"Shortener error: {e}")
        return long_url  # fallback

def generate_24h_token_url(bot_username, user_id):
    """
    Generates a 24-hour tokenized short URL for the user.
    """
    expiry_time = get_current_time() + 86400  # 24 hours in seconds
    token = str_to_b64(f"{user_id}:{expiry_time}")
    long_link = f"https://telegram.dog/{bot_username}?start=token_{token}"
    short_link = shorten_url(long_link)
    return short_link, expiry_time
  
