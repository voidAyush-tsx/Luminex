"""CSV export router endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.csv_service import export_verification_results_to_csv
from app.utils.logger import logger
import os

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/all")
def export_all(db: Session = Depends(get_db)):
    """Export all verification results to CSV."""
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
        logger.error(f"Error exporting all results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error exporting results: {str(e)}")


@router.get("/verified")
def export_verified(db: Session = Depends(get_db)):
    """Export verified (matched) results to CSV."""
    try:
        file_path = export_verification_results_to_csv(db, filter_status="matched")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="CSV file generation failed")
        
        return FileResponse(
            file_path,
            media_type="text/csv",
            filename=os.path.basename(file_path),
        )
    except Exception as e:
        logger.error(f"Error exporting verified results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error exporting verified results: {str(e)}")


@router.get("/mismatched")
def export_mismatched(db: Session = Depends(get_db)):
    """Export mismatched results to CSV."""
    try:
        file_path = export_verification_results_to_csv(db, filter_status="mismatched")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="CSV file generation failed")
        
        return FileResponse(
            file_path,
            media_type="text/csv",
            filename=os.path.basename(file_path),
        )
    except Exception as e:
        logger.error(f"Error exporting mismatched results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error exporting mismatched results: {str(e)}")

