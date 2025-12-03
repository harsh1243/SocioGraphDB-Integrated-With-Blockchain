import os

# Database and Paths
DB_PATH = "twitter_clone.db"
UPLOAD_DIR = "uploads"
PROFILE_PIC_DIR = os.path.join(UPLOAD_DIR, "profiles")
POST_IMAGE_DIR = os.path.join(UPLOAD_DIR, "posts")

# Blockchain Config
SUI_RPC_URL = "https://fullnode.mainnet.sui.io:443"

# Create directories on load
os.makedirs(PROFILE_PIC_DIR, exist_ok=True)
os.makedirs(POST_IMAGE_DIR, exist_ok=True)
