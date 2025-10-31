"""FastAPI application main entry point."""

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.database import engine, get_db
from app.models import Base
from app.routers import invoices, purchase_orders, verification, email_automation, export
from app.utils.logger import logger
from app.models.verification_result_model import VerificationResult
from app.models.invoice_model import Invoice
from app.models.purchase_order_model import PurchaseOrder
from app.utils.file_handler import save_uploaded_file, read_file_bytes, is_valid_file_type
from app.services.shivaay_ai import extract_document_data
from app.services.verification_service import compare_invoice_and_po
from app.services.csv_service import export_verification_results_to_csv
import os

# Initialize settings (may fail if env vars not set - handled in health check)
try:
    settings = get_settings()
except Exception as e:
    logger.warning(f"Settings initialization warning: {e}")
    settings = None

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"Database initialization error: {e}")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name if settings else "Futurix AI Backend",
    version=settings.app_version if settings else "1.0.0",
    description="AI-Powered Invoice & Purchase Order Verification System",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin] if settings else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(invoices.router)
app.include_router(purchase_orders.router)
app.include_router(verification.router)
app.include_router(email_automation.router)
app.include_router(export.router)


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    db_status = "connected"
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Database health check failed: {str(e)}")
    
    try:
        app_settings = get_settings()
    except:
        app_settings = None
    return {
        "app_name": app_settings.app_name if app_settings else "Futurix AI Backend",
        "version": app_settings.app_version if app_settings else "1.0.0",
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/stats", tags=["analytics"])
def get_stats(db: Session = Depends(get_db)):
    """Get verification statistics."""
    total_processed = db.query(func.count(VerificationResult.id)).scalar() or 0
    matched = db.query(func.count(VerificationResult.id)).filter(
        VerificationResult.overall_status == "matched"
    ).scalar() or 0
    mismatched = db.query(func.count(VerificationResult.id)).filter(
        VerificationResult.overall_status == "mismatched"
    ).scalar() or 0
    
    match_rate = f"{(matched / total_processed * 100):.1f}%" if total_processed > 0 else "0%"
    
    return {
        "total_processed": total_processed,
        "matched": matched,
        "mismatched": mismatched,
        "match_rate": match_rate,
    }


@app.get("/history", tags=["analytics"])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    """Get verification history."""
    verifications = db.query(VerificationResult).order_by(
        VerificationResult.created_at.desc()
    ).limit(limit).all()
    
    transactions = []
    for v in verifications:
        invoice = db.query(Invoice).filter(Invoice.id == v.invoice_id).first()
        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == v.purchase_order_id).first()
        
        transactions.append({
            "timestamp": v.created_at.strftime("%Y-%m-%d %H:%M:%S") if v.created_at else "",
            "invoice_vendor": invoice.vendor_name if invoice else "",
            "po_vendor": po.vendor_name if po else "",
            "invoice_total": str(invoice.total_amount) if invoice and invoice.total_amount else "0.00",
            "po_total": str(po.total_amount) if po and po.total_amount else "0.00",
            "status": v.overall_status,
        })
    
    return {"transactions": transactions}


@app.post("/upload_advanced", tags=["upload"])
async def upload_advanced(
    invoice: UploadFile = File(...),
    po: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and verify invoice and PO together."""
    try:
        # Validate file types
        if not is_valid_file_type(invoice.filename or ""):
            raise HTTPException(status_code=400, detail="Invalid invoice file type")
        if not is_valid_file_type(po.filename or ""):
            raise HTTPException(status_code=400, detail="Invalid PO file type")
        
        # Save files
        invoice_path = await save_uploaded_file(invoice, subdir="invoices")
        po_path = await save_uploaded_file(po, subdir="purchase_orders")
        
        # Read file bytes
        invoice_bytes = read_file_bytes(invoice_path)
        po_bytes = read_file_bytes(po_path)
        
        # Extract data from both documents
        logger.info("Extracting invoice data...")
        invoice_result = extract_document_data(invoice_bytes)
        
        logger.info("Extracting PO data...")
        po_result = extract_document_data(po_bytes)
        
        if not invoice_result.get("success"):
            raise HTTPException(status_code=500, detail=f"Invoice parsing failed: {invoice_result.get('error')}")
        
        if not po_result.get("success"):
            raise HTTPException(status_code=500, detail=f"PO parsing failed: {po_result.get('error')}")
        
        invoice_data = invoice_result.get("data", {})
        po_data = po_result.get("data", {})
        
        # Create invoice record
        invoice_record = Invoice(
            file_path=invoice_path,
            file_name=invoice.filename or "unknown",
            file_type=invoice.content_type or "",
            parsing_status="success",
            vendor_name=invoice_data.get("vendor_name"),
            vendor_address=invoice_data.get("vendor_address"),
            invoice_no=invoice_data.get("invoice_no"),
            po_no=invoice_data.get("po_no"),
            date=invoice_data.get("date"),
            due_date=invoice_data.get("due_date"),
            currency=invoice_data.get("currency"),
            subtotal=invoice_data.get("subtotal"),
            tax=invoice_data.get("tax"),
            total_amount=invoice_data.get("total_amount"),
            line_items=invoice_data.get("line_items"),
            taxes=invoice_data.get("taxes"),
            raw_data=invoice_result.get("raw_response"),
        )
        db.add(invoice_record)
        db.flush()
        
        # Create PO record
        po_record = PurchaseOrder(
            file_path=po_path,
            file_name=po.filename or "unknown",
            file_type=po.content_type or "",
            parsing_status="success",
            vendor_name=po_data.get("vendor_name"),
            vendor_address=po_data.get("vendor_address"),
            po_no=po_data.get("po_no"),
            invoice_no=po_data.get("invoice_no"),
            date=po_data.get("date"),
            due_date=po_data.get("due_date"),
            currency=po_data.get("currency"),
            subtotal=po_data.get("subtotal"),
            tax=po_data.get("tax"),
            total_amount=po_data.get("total_amount"),
            line_items=po_data.get("line_items"),
            taxes=po_data.get("taxes"),
            raw_data=po_result.get("raw_response"),
        )
        db.add(po_record)
        db.flush()
        
        # Perform comparison
        comparison_result = compare_invoice_and_po(invoice_data, po_data)
        
        # Create verification record
        verification = VerificationResult(
            invoice_id=invoice_record.id,
            purchase_order_id=po_record.id,
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
        
        # Format response to match frontend expectations
        field_comparisons = []
        for check in comparison_result["field_checks"]:
            field_comparisons.append({
                "field": check["field_key"],
                "invoice_value": check["invoice_value"],
                "po_value": check["po_value"],
                "match": check["status"] == "match",
                "difference": check.get("diff"),
            })
        
        return {
            "verification_id": verification.id,
            "invoice_id": invoice_record.id,
            "po_id": po_record.id,
            "ai_result": {
                "overall_status": comparison_result["overall_status"],
                "confidence_score": comparison_result["match_percentage"] / 100,
                "field_comparisons": field_comparisons,
                "matched_fields": comparison_result["matched_fields"],
                "total_fields": comparison_result["total_fields_checked"],
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_advanced: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/export", tags=["export"])
def export_csv(db: Session = Depends(get_db)):
    """Export all verification results to CSV (simplified endpoint for frontend)."""
    try:
        file_path = export_verification_results_to_csv(db, filter_status=None)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="CSV file generation failed")
        
        return FileResponse(
            file_path,
            media_type="text/csv",
            filename=os.path.basename(file_path),
        )
    except Exception as e:
        logger.error(f"Error exporting results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error exporting results: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

