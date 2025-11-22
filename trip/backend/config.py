import os
from dotenv import load_dotenv

ROOT_ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(ROOT_ENV_PATH)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "venus_trip")

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

    # SAFE MAX UPLOAD LIMIT (Default 200MB)
    try:
        MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 200 * 1024 * 1024))
    except:
        MAX_CONTENT_LENGTH = 200 * 1024 * 1024

    # ---------------------------------------------
    # JWT SETTINGS
    # ---------------------------------------------
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
    JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", 1440))  # 24 hours
