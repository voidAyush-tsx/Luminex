"""Invoice router endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import InvoiceResponse, InvoiceCreate
from app.models.invoice_model import Invoice
from app.utils.file_handler import save_uploaded_file, read_file_bytes, is_valid_file_type
from app.services.shivaay_ai import extract_document_data
from app.utils.logger import logger
from app.core.celery_app import celery_app
from app.services.shivaay_ai import parse_and_verify_document

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all invoices."""
    invoices = db.query(Invoice).offset(skip).limit(limit).all()
    return invoices


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Get invoice by ID."""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse invoice file."""
    # Validate file type
    if not is_valid_file_type(file.filename or ""):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: PDF, PNG, JPG, JPEG, TIFF"
        )
    
    try:
        # Save file
        file_path = await save_uploaded_file(file, subdir="invoices")
        file_bytes = read_file_bytes(file_path)
        
        # Create invoice record
        invoice = Invoice(
            file_path=file_path,
            file_name=file.filename or "unknown",
            file_type=file.content_type or "",
            parsing_status="processing",
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        
        # Parse document asynchronously via Celery
        from app.core.celery_app import celery_app
        celery_app.send_task("parse_and_verify_document", args=[file_bytes, None])
        
        # Alternatively, parse synchronously:
        # result = extract_document_data(file_bytes)
        # if result.get("success"):
        #     data = result.get("data", {})
        #     for key, value in data.items():
        #         if hasattr(invoice, key):
        #             setattr(invoice, key, value)
        #     invoice.parsing_status = "success"
        # else:
        #     invoice.parsing_status = "failed"
        #     invoice.parsing_error = result.get("error")
        # db.commit()
        
        return invoice
    except Exception as e:
        logger.error(f"Error creating invoice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing invoice: {str(e)}")


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Delete invoice by ID."""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    db.delete(invoice)
    db.commit()
    return None

