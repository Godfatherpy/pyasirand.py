import base64
import time
from typing import Optional

def str_to_b64(s: str) -> str:
    """Encode a string to a URL-safe base64 string."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return base64.urlsafe_b64encode(s.encode('utf-8')).decode('utf-8')

def b64_to_str(b64: str) -> Optional[str]:
    """Decode a URL-safe base64 string to a regular string.
    
    Returns None if decoding fails.
    """
    try:
        return base64.urlsafe_b64decode(b64.encode('utf-8')).decode('utf-8')
    except Exception:
        return None

def get_current_time() -> int:
    """Get current UNIX timestamp in seconds."""
    return int(time.time())
