"""
File Handling Utilities
"""

import os
import shutil
from typing import Optional
from pathlib import Path


def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if not"""
    os.makedirs(path, exist_ok=True)


def save_uploaded_file(upload_file, destination: str) -> str:
    """
    Save uploaded file to destination

    Args:
        upload_file: UploadFile object
        destination: Destination file path

    Returns:
        Path to saved file
    """
    ensure_directory(os.path.dirname(destination))

    with open(destination, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

    return destination


def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """
    Validate file extension

    Args:
        filename: Name of file
        allowed_extensions: Set of allowed extensions (e.g., {'.pdf', '.png'})

    Returns:
        True if valid, False otherwise
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions


def cleanup_old_files(directory: str, days: int = 7) -> int:
    """
    Clean up files older than specified days

    Args:
        directory: Directory to clean
        days: Age threshold in days

    Returns:
        Number of files deleted
    """
    import time

    if not os.path.exists(directory):
        return 0

    current_time = time.time()
    threshold = days * 86400  # days to seconds
    deleted_count = 0

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath):
            file_age = current_time - os.path.getmtime(filepath)

            if file_age > threshold:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")

    return deleted_count


def get_file_size_mb(filepath: str) -> float:
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

