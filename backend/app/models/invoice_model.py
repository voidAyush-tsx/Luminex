"""Invoice database model."""

from sqlalchemy import Column, String, Numeric, Text, JSON
from app.models.base import BaseModel


class Invoice(BaseModel):
    """Invoice model storing parsed invoice data."""
    
    __tablename__ = "invoices"
    
    # Document metadata
    file_path = Column(String(500), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=True)
    
    # Parsed fields from Shivaay AI
    vendor_name = Column(String(255), nullable=True)
    vendor_address = Column(Text, nullable=True)
    invoice_no = Column(String(100), nullable=True, unique=True, index=True)
    po_no = Column(String(100), nullable=True, index=True)
    date = Column(String(50), nullable=True)  # ISO date string
    due_date = Column(String(50), nullable=True)
    currency = Column(String(10), default="USD")
    subtotal = Column(Numeric(15, 2), nullable=True)
    tax = Column(Numeric(15, 2), nullable=True)
    total_amount = Column(Numeric(15, 2), nullable=True)
    
    # Structured data (JSON)
    line_items = Column(JSON, nullable=True)  # List of dicts: {description, qty, unit_price}
    taxes = Column(JSON, nullable=True)  # List of tax details
    raw_data = Column(JSON, nullable=True)  # Full parsed response from Shivaay
    
    # Status
    parsing_status = Column(String(50), default="pending")  # pending, success, failed
    parsing_error = Column(Text, nullable=True)

