"""CSV export service using Pandas."""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.celery_app import celery_app
from app.utils.logger import logger
from app.models.verification_result_model import VerificationResult
from app.models.invoice_model import Invoice
from app.models.purchase_order_model import PurchaseOrder

settings = get_settings()


def export_verification_results_to_csv(
    db: Session,
    filter_status: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Export verification results to CSV file.
    
    Args:
        db: Database session
        filter_status: Optional filter by status (matched, mismatched, partial)
        output_path: Optional output file path
    
    Returns:
        Path to generated CSV file
    """
    # Query verification results with joins
    query = db.query(VerificationResult).join(Invoice).join(PurchaseOrder)
    
    if filter_status:
        query = query.filter(VerificationResult.overall_status == filter_status)
    
    results = query.all()
    
    # Build data rows
    rows = []
    for result in results:
        invoice = result.invoice
        po = result.purchase_order
        
        row = {
            "verification_id": result.id,
            "verification_status": result.overall_status,
            "verification_date": result.created_at.isoformat() if result.created_at else None,
            "matched_fields": result.matched_fields,
            "mismatched_fields": result.mismatched_fields,
            "total_fields_checked": result.total_fields_checked,
            # Invoice fields
            "invoice_id": invoice.id,
            "invoice_no": invoice.invoice_no,
            "invoice_vendor": invoice.vendor_name,
            "invoice_date": invoice.date,
            "invoice_total": float(invoice.total_amount) if invoice.total_amount else None,
            "invoice_currency": invoice.currency,
            # PO fields
            "po_id": po.id,
            "po_no": po.po_no,
            "po_vendor": po.vendor_name,
            "po_date": po.date,
            "po_total": float(po.total_amount) if po.total_amount else None,
            "po_currency": po.currency,
            # Comparison
            "total_match": invoice.total_amount == po.total_amount if (invoice.total_amount and po.total_amount) else False,
        }
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Generate output path if not provided
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status_suffix = f"_{filter_status}" if filter_status else ""
        filename = f"verification_results{status_suffix}_{timestamp}.csv"
        output_path = os.path.join(settings.export_dir, filename)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Exported {len(rows)} verification results to {output_path}")
    
    return output_path


@celery_app.task(name="generate_csv_snapshot")
def generate_csv_snapshot():
    """Celery Beat task to generate CSV snapshots."""
    logger.info("Generating CSV snapshot")
    
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Generate all exports
        export_verification_results_to_csv(db, filter_status=None)
        export_verification_results_to_csv(db, filter_status="matched")
        export_verification_results_to_csv(db, filter_status="mismatched")
        logger.info("CSV snapshot generation completed")
    except Exception as e:
        logger.error(f"Error generating CSV snapshot: {str(e)}")
    finally:
        db.close()

