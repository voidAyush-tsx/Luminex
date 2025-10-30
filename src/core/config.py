"""
Configuration Settings for Futurix AI
Centralized configuration management
"""

import os
from typing import Dict, Any
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    """Application settings"""

    # Application Info
    APP_NAME = "Futurix AI - Invoice & PO Verification"
    VERSION = "1.0.0"
    DESCRIPTION = "AI-powered invoice and purchase order verification system"

    # Server Settings
    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = True

    # Directories (using new structure)
    UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
    EXPORT_DIR = os.path.join(BASE_DIR, "data", "exports")
    SAMPLE_DIR = os.path.join(BASE_DIR, "data", "samples")

    # File Settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg'}

    # OCR Settings (Shivaay AI)
    SHIVAAY_API_BASE = "https://shivaay.futurixai.com"
    SHIVAAY_API_KEY = os.getenv("SHIVAAY_API_KEY", "")
    OCR_MODEL = "gpt-4o"  # Shivaay AI vision model
    OCR_DPI = 300  # For PDF to image conversion

    # Comparison Tolerances
    VENDOR_FUZZY_THRESHOLD = 85  # Percentage (0-100)
    AMOUNT_TOLERANCE_PERCENT = 0.5  # Percentage
    DATE_TOLERANCE_DAYS = 3  # Days

    # CSV Export Settings
    CSV_ENCODING = 'utf-8'
    CSV_INDEX = False

    # Gmail Settings
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    GMAIL_SEARCH_QUERY = 'has:attachment (invoice OR "purchase order") newer_than:7d'
    GMAIL_MAX_RESULTS = 20

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # CORS
    CORS_ORIGINS = ["*"]  # For production, restrict this
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    @classmethod
    def get_shivaay_api_key(cls) -> str:
        """Get Shivaay API key from environment or config file"""
        # Try environment variable first
        api_key = os.getenv("SHIVAAY_API_KEY")
        if api_key:
            return api_key

        # Try config file
        config_file = os.path.join(BASE_DIR, "shivaay_config.txt")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return f.read().strip()

        return ""

    @classmethod
    def get_comparison_config(cls) -> Dict[str, Any]:
        """Get comparison configuration"""
        return {
            "vendor_threshold": cls.VENDOR_FUZZY_THRESHOLD,
            "amount_tolerance": cls.AMOUNT_TOLERANCE_PERCENT,
            "date_tolerance": cls.DATE_TOLERANCE_DAYS
        }


# Create settings instance
settings = Settings()

