"""Email automation router endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import EmailSyncResponse
from app.services.email_service import search_emails, periodic_email_scan
from app.utils.logger import logger
from app.core.celery_app import celery_app

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/sync", response_model=EmailSyncResponse)
def sync_emails(db: Session = Depends(get_db)):
    """Trigger manual email sync (enqueues Celery task)."""
    try:
        # Enqueue email scan task
        from app.core.celery_app import celery_app
        task = celery_app.send_task("periodic_email_scan")
        
        # For immediate sync, we can also search synchronously (but async via Celery is preferred)
        emails = search_emails(max_results=50)
        
        return EmailSyncResponse(
            message="Email sync task enqueued",
            emails_found=len(emails),
            emails_processed=0,  # Will be updated by task
        )
    except Exception as e:
        logger.error(f"Error syncing emails: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error syncing emails: {str(e)}")


@router.get("/status")
def email_status():
    """Get email sync status (placeholder)."""
    return {
        "status": "active",
        "last_sync": None,  # Could be tracked in DB
    }

