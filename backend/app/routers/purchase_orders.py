"""Purchase Order router endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PurchaseOrderResponse, PurchaseOrderCreate
from app.models.purchase_order_model import PurchaseOrder
from app.utils.file_handler import save_uploaded_file, read_file_bytes, is_valid_file_type
from app.services.shivaay_ai import extract_document_data
from app.utils.logger import logger
from app.core.celery_app import celery_app
from app.services.shivaay_ai import parse_and_verify_document

router = APIRouter(prefix="/purchase-orders", tags=["purchase-orders"])


@router.get("/", response_model=List[PurchaseOrderResponse])
def list_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all purchase orders."""
    pos = db.query(PurchaseOrder).offset(skip).limit(limit).all()
    return pos


@router.get("/{po_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(po_id: int, db: Session = Depends(get_db)):
    """Get purchase order by ID."""
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po


@router.post("/", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse purchase order file."""
    # Validate file type
    if not is_valid_file_type(file.filename or ""):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: PDF, PNG, JPG, JPEG, TIFF"
        )
    
    try:
        # Save file
        file_path = await save_uploaded_file(file, subdir="purchase_orders")
        file_bytes = read_file_bytes(file_path)
        
        # Create PO record
        po = PurchaseOrder(
            file_path=file_path,
            file_name=file.filename or "unknown",
            file_type=file.content_type or "",
            parsing_status="processing",
        )
        db.add(po)
        db.commit()
        db.refresh(po)
        
        # Parse document asynchronously via Celery
        from app.core.celery_app import celery_app
        celery_app.send_task("parse_and_verify_document", args=[file_bytes, None])
        
        return po
    except Exception as e:
        logger.error(f"Error creating purchase order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing purchase order: {str(e)}")


@router.delete("/{po_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_order(po_id: int, db: Session = Depends(get_db)):
    """Delete purchase order by ID."""
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    db.delete(po)
    db.commit()
    return None

