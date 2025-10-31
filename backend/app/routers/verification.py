"""Verification router endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import VerificationRequest, VerificationResponse
from app.models.verification_result_model import VerificationResult
from app.models.invoice_model import Invoice
from app.models.purchase_order_model import PurchaseOrder
from app.services.verification_service import compare_invoice_and_po
from app.utils.logger import logger

router = APIRouter(prefix="/verify", tags=["verification"])


@router.post("/", response_model=VerificationResponse, status_code=status.HTTP_201_CREATED)
def verify_documents(
    request: VerificationRequest,
    db: Session = Depends(get_db)
):
    """Compare invoice and purchase order."""
    # Fetch invoice and PO
    invoice = db.query(Invoice).filter(Invoice.id == request.invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == request.purchase_order_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    # Convert models to dicts for comparison
    invoice_dict = {
        "vendor_name": invoice.vendor_name,
        "vendor_address": invoice.vendor_address,
        "po_no": invoice.po_no,
        "date": invoice.date,
        "currency": invoice.currency,
        "subtotal": invoice.subtotal,
        "tax": invoice.tax,
        "total_amount": invoice.total_amount,
        "line_items": invoice.line_items or [],
    }
    
    po_dict = {
        "vendor_name": po.vendor_name,
        "vendor_address": po.vendor_address,
        "po_no": po.po_no,
        "date": po.date,
        "currency": po.currency,
        "subtotal": po.subtotal,
        "tax": po.tax,
        "total_amount": po.total_amount,
        "line_items": po.line_items or [],
    }
    
    # Perform comparison
    comparison_result = compare_invoice_and_po(invoice_dict, po_dict)
    
    # Save verification result
    verification = VerificationResult(
        invoice_id=invoice.id,
        purchase_order_id=po.id,
        overall_status=comparison_result["overall_status"],
        field_checks=comparison_result["field_checks"],
        total_fields_checked=comparison_result["total_fields_checked"],
        matched_fields=comparison_result["matched_fields"],
        mismatched_fields=comparison_result["mismatched_fields"],
        raw_verification_data=comparison_result,
    )
    
    db.add(verification)
    db.commit()
    db.refresh(verification)
    
    return verification


@router.get("/", response_model=List[VerificationResponse])
def list_verifications(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """List all verification results."""
    query = db.query(VerificationResult)
    
    if status_filter:
        query = query.filter(VerificationResult.overall_status == status_filter)
    
    results = query.order_by(VerificationResult.created_at.desc()).offset(skip).limit(limit).all()
    return results


@router.get("/{verification_id}", response_model=VerificationResponse)
def get_verification(verification_id: int, db: Session = Depends(get_db)):
    """Get verification result by ID."""
    verification = db.query(VerificationResult).filter(VerificationResult.id == verification_id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification result not found")
    return verification

