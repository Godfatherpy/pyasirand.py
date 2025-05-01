import requests
from urllib.parse import quote
from helper import str_to_b64, get_current_time

def shorten_url(long_url: str) -> str:
    """
    Shortens URLs using custom shortener service with HTML response prevention
    Returns original URL (converted to t.me) if shortening fails
    """
    try:
        # Encode URL and prepare API request
        encoded_url = quote(long_url, safe='')
        api_url = f"YOUR_CUSTOM_API_ENDPOINT?url={encoded_url}"  # Replace with your actual API URL
        
        # Force text/plain response if possible
        headers = {'Accept': 'text/plain'}
        
        response = requests.get(
            api_url,
            timeout=10,
            headers=headers
        )

        # Reject HTML responses immediately
        if 'text/html' in response.headers.get('Content-Type', ''):
            raise ValueError("Received HTML response from shortener")

        # Handle successful responses
        if response.status_code == 200:
            # Try JSON first
            try:
                return response.json()['short_url']  # Replace 'short_url' with your API's key
            except ValueError:
                # Fallback to text response
                short_url = response.text.strip()
                # Validate URL format
                if short_url.startswith(('http://', 'https://')):
                    return short_url

        return long_url.replace("telegram.dog", "t.me")
    
    except Exception as e:
        print(f"Shortening error: {str(e)}")
        return long_url.replace("telegram.dog", "t.me")

def generate_24h_token_url(bot_username: str, user_id: int) -> tuple:
    """
    Generates refresh URLs with enhanced HTML protection
    Returns tuple: (url, expiry_timestamp)
    """
    expiry_time = get_current_time() + 86400
    token = str_to_b64(f"{user_id}:{expiry_time}")
    
    # Force t.me domain for base URL
    base_url = f"https://t.me/{bot_username}?start=token_{token}"
    
    # Shortening logic with HTML prevention
    if len(base_url) > 60:  # Only shorten if necessary
        shortened = shorten_url(base_url)
        
        # Final HTML check before returning
        if '<!DOCTYPE html>' in shortened.lower():
            return base_url, expiry_time
        return shortened, expiry_time
    
    return base_url, expiry_time
