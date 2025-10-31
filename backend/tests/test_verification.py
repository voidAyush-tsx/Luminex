"""Verification service tests."""

import pytest
from decimal import Decimal
from app.services.verification_service import compare_invoice_and_po


def test_verification_matched():
    """Test verification with matching documents."""
    invoice = {
        "vendor_name": "Test Vendor",
        "vendor_address": "123 Main St",
        "po_no": "PO-001",
        "date": "2024-01-15",
        "currency": "USD",
        "subtotal": Decimal("1000.00"),
        "tax": Decimal("100.00"),
        "total_amount": Decimal("1100.00"),
        "line_items": [],
    }
    
    po = {
        "vendor_name": "Test Vendor",
        "vendor_address": "123 Main St",
        "po_no": "PO-001",
        "date": "2024-01-15",
        "currency": "USD",
        "subtotal": Decimal("1000.00"),
        "tax": Decimal("100.00"),
        "total_amount": Decimal("1100.00"),
        "line_items": [],
    }
    
    result = compare_invoice_and_po(invoice, po)
    assert result["overall_status"] == "matched"
    assert result["matched_fields"] > 0
    assert result["mismatched_fields"] == 0


def test_verification_mismatched():
    """Test verification with mismatched documents."""
    invoice = {
        "vendor_name": "Test Vendor",
        "vendor_address": "123 Main St",
        "po_no": "PO-001",
        "date": "2024-01-15",
        "currency": "USD",
        "subtotal": Decimal("1000.00"),
        "tax": Decimal("100.00"),
        "total_amount": Decimal("1100.00"),
        "line_items": [],
    }
    
    po = {
        "vendor_name": "Test Vendor",
        "vendor_address": "123 Main St",
        "po_no": "PO-001",
        "date": "2024-01-15",
        "currency": "USD",
        "subtotal": Decimal("2000.00"),  # Different amount
        "tax": Decimal("200.00"),
        "total_amount": Decimal("2200.00"),  # Different total
        "line_items": [],
    }
    
    result = compare_invoice_and_po(invoice, po)
    assert result["overall_status"] in ["mismatched", "partial"]
    assert result["mismatched_fields"] > 0

