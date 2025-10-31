"""Verification service for comparing invoices and purchase orders."""

from typing import Dict, Any, List
from decimal import Decimal
from app.utils.logger import logger
from app.utils.validators import parse_decimal


def compare_invoice_and_po(invoice: Dict[str, Any], po: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare invoice and purchase order data.
    
    Args:
        invoice: Invoice data dictionary
        po: Purchase order data dictionary
    
    Returns:
        Dictionary with comparison results including field checks and overall status
    """
    field_checks: List[Dict[str, Any]] = []
    
    # Fields to compare
    fields_to_compare = [
        ("vendor_name", "Vendor Name"),
        ("vendor_address", "Vendor Address"),
        ("po_no", "PO Number"),
        ("date", "Date"),
        ("currency", "Currency"),
        ("subtotal", "Subtotal"),
        ("tax", "Tax"),
        ("total_amount", "Total Amount"),
    ]
    
    matched_count = 0
    mismatched_count = 0
    
    for field_key, field_name in fields_to_compare:
        invoice_value = invoice.get(field_key)
        po_value = po.get(field_key)
        
        status = "match"
        diff = None
        
        # Compare values
        if invoice_value is None and po_value is None:
            status = "match"
        elif invoice_value is None or po_value is None:
            status = "mismatch"
            mismatched_count += 1
        else:
            # For numeric fields, allow small tolerance
            if field_key in ["subtotal", "tax", "total_amount"]:
                inv_val = parse_decimal(invoice_value)
                po_val = parse_decimal(po_value)
                
                if inv_val is None or po_val is None:
                    status = "mismatch" if invoice_value != po_value else "match"
                else:
                    # Allow 0.01 tolerance for floating point errors
                    diff = float(abs(inv_val - po_val))
                    if diff <= 0.01:
                        status = "match"
                        matched_count += 1
                    else:
                        status = "mismatch"
                        mismatched_count += 1
            else:
                # String comparison (case-insensitive, trimmed)
                inv_str = str(invoice_value).strip().lower() if invoice_value else ""
                po_str = str(po_value).strip().lower() if po_value else ""
                
                if inv_str == po_str:
                    status = "match"
                    matched_count += 1
                else:
                    status = "mismatch"
                    mismatched_count += 1
        
        field_checks.append({
            "field": field_name,
            "field_key": field_key,
            "invoice_value": invoice_value,
            "po_value": po_value,
            "status": status,
            "diff": diff,
        })
    
    # Compare line items (optional, more complex)
    line_items_match = compare_line_items(
        invoice.get("line_items", []),
        po.get("line_items", [])
    )
    
    if line_items_match is not None:
        field_checks.append(line_items_match)
        if line_items_match.get("status") == "match":
            matched_count += 1
        else:
            mismatched_count += 1
    
    # Determine overall status
    total_fields = len(field_checks)
    if mismatched_count == 0:
        overall_status = "matched"
    elif matched_count == 0:
        overall_status = "mismatched"
    else:
        overall_status = "partial"
    
    return {
        "overall_status": overall_status,
        "field_checks": field_checks,
        "total_fields_checked": total_fields,
        "matched_fields": matched_count,
        "mismatched_fields": mismatched_count,
        "match_percentage": (matched_count / total_fields * 100) if total_fields > 0 else 0,
    }


def compare_line_items(invoice_items: List[Dict], po_items: List[Dict]) -> Dict[str, Any]:
    """Compare line items between invoice and PO."""
    if not invoice_items and not po_items:
        return None
    
    if len(invoice_items) != len(po_items):
        return {
            "field": "Line Items",
            "field_key": "line_items",
            "invoice_value": f"{len(invoice_items)} items",
            "po_value": f"{len(po_items)} items",
            "status": "mismatch",
            "diff": None,
        }
    
    # Simple comparison - check if total quantities and amounts match
    inv_total_qty = sum(parse_decimal(item.get("qty", 0)) or Decimal(0) for item in invoice_items)
    po_total_qty = sum(parse_decimal(item.get("qty", 0)) or Decimal(0) for item in po_items)
    
    if abs(float(inv_total_qty - po_total_qty)) > 0.01:
        return {
            "field": "Line Items",
            "field_key": "line_items",
            "invoice_value": f"{len(invoice_items)} items, total qty: {inv_total_qty}",
            "po_value": f"{len(po_items)} items, total qty: {po_total_qty}",
            "status": "mismatch",
            "diff": float(abs(inv_total_qty - po_total_qty)),
        }
    
    return {
        "field": "Line Items",
        "field_key": "line_items",
        "invoice_value": f"{len(invoice_items)} items",
        "po_value": f"{len(po_items)} items",
        "status": "match",
        "diff": None,
    }

