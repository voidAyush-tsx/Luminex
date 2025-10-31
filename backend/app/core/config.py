"""Application configuration loaded from environment variables."""

import os
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # App info
    app_name: str = "Futurix AI Backend"
    app_version: str = "1.0.0"
    
    # Shivaay AI
    shivaay_api_key: str = os.getenv("SHIVAAY_API_KEY", "")
    shivaay_base_url: str = "https://api.futurixai.com/api/shivaay/v1"
    
    # Gmail OAuth2
    gmail_client_id: str = os.getenv("GMAIL_CLIENT_ID", "")
    gmail_client_secret: str = os.getenv("GMAIL_CLIENT_SECRET", "")
    gmail_refresh_token: str = os.getenv("GMAIL_REFRESH_TOKEN", "")
    
    # Security
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # CORS
    cors_origin: str = os.getenv("CORS_ORIGIN", "http://localhost:3000")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./futurix.db")
    
    # Celery (default to in-memory for local dev if Redis not available)
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # File storage
    upload_dir: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    export_dir: str = os.getenv("EXPORT_DIR", "./data/exports")
    
    def __init__(self):
        """Validate required settings."""
        required = [
            "shivaay_api_key",
            "gmail_client_id",
            "gmail_client_secret",
            "gmail_refresh_token",
            "jwt_secret_key",
        ]
        missing = [key for key in required if not getattr(self, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create directories on first access
def _ensure_directories():
    """Ensure required directories exist."""
    try:
        settings = get_settings()
        os.makedirs(settings.upload_dir, exist_ok=True)
        os.makedirs(settings.export_dir, exist_ok=True)
    except ValueError:
        # Settings not fully configured yet, skip directory creation
        pass

