"""Verification Result database model."""

from sqlalchemy import Column, String, Text, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class VerificationResult(BaseModel):
    """Verification result model comparing invoice and PO."""
    
    __tablename__ = "verification_results"
    
    # Foreign keys
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False, index=True)
    
    # Verification status
    overall_status = Column(String(50), nullable=False)  # matched, mismatched, partial
    
    # Verification details (JSON)
    field_checks = Column(JSON, nullable=True)  # List of dicts: {field, invoice_value, po_value, status, diff}
    
    # Summary
    total_fields_checked = Column(Integer, default=0)
    matched_fields = Column(Integer, default=0)
    mismatched_fields = Column(Integer, default=0)
    
    # Additional metadata
    verification_notes = Column(Text, nullable=True)
    raw_verification_data = Column(JSON, nullable=True)  # Full comparison result
    
    # Relationships
    invoice = relationship("Invoice", backref="verification_results")
    purchase_order = relationship("PurchaseOrder", backref="verification_results")

