"""Pydantic schemas for request/response validation."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


# Invoice schemas
class InvoiceBase(BaseModel):
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    invoice_no: Optional[str] = None
    po_no: Optional[str] = None
    date: Optional[str] = None
    due_date: Optional[str] = None
    currency: Optional[str] = "USD"
    subtotal: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    line_items: Optional[List[Dict[str, Any]]] = None
    taxes: Optional[List[Dict[str, Any]]] = None


class InvoiceCreate(InvoiceBase):
    file_path: str
    file_name: str
    file_type: Optional[str] = None


class InvoiceResponse(InvoiceBase):
    id: int
    file_path: str
    file_name: str
    file_type: Optional[str] = None
    parsing_status: str
    parsing_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Purchase Order schemas
class PurchaseOrderBase(BaseModel):
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    po_no: Optional[str] = None
    invoice_no: Optional[str] = None
    date: Optional[str] = None
    due_date: Optional[str] = None
    currency: Optional[str] = "USD"
    subtotal: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    line_items: Optional[List[Dict[str, Any]]] = None
    taxes: Optional[List[Dict[str, Any]]] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    file_path: str
    file_name: str
    file_type: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    file_path: str
    file_name: str
    file_type: Optional[str] = None
    parsing_status: str
    parsing_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Verification schemas
class VerificationRequest(BaseModel):
    invoice_id: int
    purchase_order_id: int


class FieldCheck(BaseModel):
    field: str
    field_key: str
    invoice_value: Any
    po_value: Any
    status: str
    diff: Optional[float] = None


class VerificationResponse(BaseModel):
    id: int
    invoice_id: int
    purchase_order_id: int
    overall_status: str
    field_checks: List[Dict[str, Any]]
    total_fields_checked: int
    matched_fields: int
    mismatched_fields: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Email schemas
class EmailSyncResponse(BaseModel):
    message: str
    emails_found: int
    emails_processed: int


# Health check schema
class HealthResponse(BaseModel):
    app_name: str
    version: str
    status: str
    database: str
    timestamp: datetime

