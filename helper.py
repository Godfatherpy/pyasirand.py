# helper.py

import base64
import time

def str_to_b64(s: str) -> str:
    """Encode string to base64."""
    return base64.urlsafe_b64encode(s.encode()).decode()

def b64_to_str(b64: str) -> str:
    """Decode base64 string."""
    return base64.urlsafe_b64decode(b64.encode()).decode()

def get_current_time() -> int:
    """Get current UNIX timestamp in seconds."""
    return int(time.time())
  
