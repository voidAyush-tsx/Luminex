"""File handling utilities."""

import os
import uuid
from pathlib import Path
from typing import Optional
from datetime import datetime
import aiofiles
from fastapi import UploadFile
from app.core.config import get_settings

settings = get_settings()


async def save_uploaded_file(file: UploadFile, subdir: Optional[str] = None) -> str:
    """Save uploaded file and return file path."""
    # Generate unique filename
    file_ext = Path(file.filename).suffix if file.filename else ""
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    
    # Determine save directory
    save_dir = settings.upload_dir
    if subdir:
        save_dir = os.path.join(save_dir, subdir)
    
    os.makedirs(save_dir, exist_ok=True)
    
    file_path = os.path.join(save_dir, unique_name)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return file_path


def read_file_bytes(file_path: str) -> bytes:
    """Read file as bytes."""
    with open(file_path, 'rb') as f:
        return f.read()


def delete_file(file_path: str) -> bool:
    """Delete file if it exists."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def is_valid_file_type(filename: str, allowed_extensions: list = None) -> bool:
    """Check if file extension is allowed."""
    if allowed_extensions is None:
        allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif']
    
    ext = get_file_extension(filename)
    return ext in allowed_extensions

