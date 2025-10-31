"""Validation utilities."""

from typing import Any, Optional
from decimal import Decimal, InvalidOperation
from datetime import datetime


def parse_decimal(value: Any) -> Optional[Decimal]:
    """Parse value to Decimal, handling various input types."""
    if value is None:
        return None
    
    if isinstance(value, Decimal):
        return value
    
    if isinstance(value, (int, float)):
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None
    
    if isinstance(value, str):
        # Remove currency symbols, commas, whitespace
        cleaned = value.replace('$', '').replace(',', '').strip()
        try:
            return Decimal(cleaned)
        except (InvalidOperation, ValueError):
            return None
    
    return None


def parse_date(date_str: Optional[str]) -> Optional[str]:
    """Parse date string and return ISO format string."""
    if not date_str:
        return None
    
    # Common date formats
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y-%m-%dT%H:%M:%S",
        "%d-%m-%Y",
        "%m-%d-%Y",
    ]
    
    if isinstance(date_str, str):
        date_str = date_str.strip()
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.isoformat()
        except (ValueError, TypeError):
            continue
    
    # Return as-is if parsing fails
    return date_str


def normalize_string(value: Any) -> Optional[str]:
    """Normalize string value."""
    if value is None:
        return None
    
    if isinstance(value, str):
        return value.strip()
    
    return str(value).strip() if value else None

