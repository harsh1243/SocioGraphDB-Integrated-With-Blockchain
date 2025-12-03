import hashlib
import time
import base64
from datetime import datetime

def hash_password(password: str) -> str:
    """Hashes a password for storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def now_ts() -> float:
    """Returns current timestamp."""
    return time.time()

def human_time(ts: float) -> str:
    """Converts timestamp to human readable string."""
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%Y-%m-%d %H:%M")

def get_image_base64(path):
    """Converts an image file to a base64 string for HTML rendering."""
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return None
