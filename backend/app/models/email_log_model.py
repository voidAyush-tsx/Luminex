"""Email Log database model."""

from sqlalchemy import Column, String, Text, JSON, DateTime, Integer
from app.models.base import BaseModel


class EmailLog(BaseModel):
    """Email log model tracking email sync operations."""
    
    __tablename__ = "email_logs"
    
    # Email metadata
    email_id = Column(String(255), nullable=False, unique=True, index=True)
    subject = Column(String(500), nullable=True)
    sender = Column(String(255), nullable=True)
    received_at = Column(DateTime, nullable=True)
    
    # Processing status
    status = Column(String(50), default="pending")  # pending, processed, failed, skipped
    error_message = Column(Text, nullable=True)
    
    # Attachment info
    attachment_count = Column(Integer, default=0)
    attachments = Column(JSON, nullable=True)  # List of {filename, file_path, processed}
    
    # Sync metadata
    sync_type = Column(String(50), nullable=True)  # manual, automatic
    processed_at = Column(DateTime, nullable=True)

