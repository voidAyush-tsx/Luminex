"""Email service for Gmail integration and automation."""

import os
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any, Optional
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.core.config import get_settings
from app.core.celery_app import celery_app
from app.utils.logger import logger
from app.utils.file_handler import save_uploaded_file, read_file_bytes

settings = get_settings()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_gmail_service() -> Any:
    """Get authenticated Gmail API service."""
    creds = None
    
    # Try to use refresh token directly
    if settings.gmail_refresh_token:
        creds = Credentials(
            token=None,
            refresh_token=settings.gmail_refresh_token,
            client_id=settings.gmail_client_id,
            client_secret=settings.gmail_client_secret,
            token_uri='https://oauth2.googleapis.com/token',
        )
        
        # Refresh token if expired
        if creds.expired:
            creds.refresh(Request())
    
    if not creds or not creds.valid:
        logger.error("Gmail credentials not valid")
        raise ValueError("Gmail credentials not valid")
    
    return build('gmail', 'v1', credentials=creds)


def get_gmail_service_imap() -> imaplib.IMAP4_SSL:
    """Get Gmail IMAP connection as fallback."""
    # Note: This requires app-specific password if 2FA is enabled
    # For now, we'll use OAuth2 primarily
    raise NotImplementedError("IMAP fallback requires additional configuration")


def search_emails(query: str = "has:attachment (invoice OR 'purchase order' OR po)", max_results: int = 10) -> List[Dict[str, Any]]:
    """Search for emails matching query."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        email_list = []
        
        for msg in messages:
            try:
                message = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()
                
                # Extract headers
                headers = message['payload'].get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
                date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                # Parse attachments
                attachments = extract_attachments(service, msg['id'], message['payload'])
                
                email_list.append({
                    'id': msg['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': date_str,
                    'attachments': attachments,
                })
            except Exception as e:
                logger.error(f"Error processing email {msg['id']}: {str(e)}")
                continue
        
        return email_list
    except Exception as e:
        logger.error(f"Error searching emails: {str(e)}")
        return []


def extract_attachments(service: Any, message_id: str, payload: Dict) -> List[Dict[str, Any]]:
    """Extract attachments from email message."""
    attachments = []
    
    def get_attachments_from_parts(parts: List[Dict]) -> None:
        for part in parts:
            if part.get('filename'):
                attachment_id = part['body'].get('attachmentId')
                if attachment_id:
                    try:
                        att = service.users().messages().attachments().get(
                            userId='me',
                            messageId=message_id,
                            id=attachment_id
                        ).execute()
                        
                        file_data = att['data']
                        import base64
                        file_bytes = base64.urlsafe_b64decode(file_data)
                        
                        attachments.append({
                            'filename': part['filename'],
                            'size': part['body'].get('size', 0),
                            'mime_type': part.get('mimeType', ''),
                            'data': file_bytes,
                        })
                    except Exception as e:
                        logger.error(f"Error extracting attachment: {str(e)}")
            
            if 'parts' in part:
                get_attachments_from_parts(part['parts'])
    
    if 'parts' in payload:
        get_attachments_from_parts(payload['parts'])
    elif payload.get('filename'):
        # Single attachment
        attachment_id = payload['body'].get('attachmentId')
        if attachment_id:
            try:
                att = service.users().messages().attachments().get(
                    userId='me',
                    messageId=message_id,
                    id=attachment_id
                ).execute()
                
                file_data = att['data']
                import base64
                file_bytes = base64.urlsafe_b64decode(file_data)
                
                attachments.append({
                    'filename': payload['filename'],
                    'size': payload['body'].get('size', 0),
                    'mime_type': payload.get('mimeType', ''),
                    'data': file_bytes,
                })
            except Exception as e:
                logger.error(f"Error extracting attachment: {str(e)}")
    
    return attachments


@celery_app.task(name="periodic_email_scan")
def periodic_email_scan():
    """Celery task for periodic email scanning."""
    logger.info("Starting periodic email scan")
    
    emails = search_emails(query="is:unread has:attachment (invoice OR 'purchase order' OR po)")
    
    for email_data in emails:
        try:
            # Create email log entry
            from app.database import SessionLocal
            from app.models.email_log_model import EmailLog
            
            db = SessionLocal()
            try:
                # Check if email already processed
                existing = db.query(EmailLog).filter(EmailLog.email_id == email_data['id']).first()
                if existing:
                    continue
                
                email_log = EmailLog(
                    email_id=email_data['id'],
                    subject=email_data['subject'],
                    sender=email_data['sender'],
                    attachment_count=len(email_data['attachments']),
                    attachments=[{"filename": att['filename'], "processed": False} for att in email_data['attachments']],
                    sync_type="automatic",
                    status="pending",
                )
                db.add(email_log)
                db.commit()
                db.refresh(email_log)
                
                # Process attachments
                from app.core.celery_app import celery_app
                parse_task = celery_app.send_task(
                    "parse_and_verify_document",
                    args=[attachment['data'], email_log.id]
                )
                logger.info(f"Enqueued parse task {parse_task.id} for attachment {attachment['filename']}")
                
                email_log.status = "processed"
                email_log.processed_at = datetime.utcnow()
                db.commit()
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error processing email {email_data['id']}: {str(e)}")
    
    logger.info(f"Periodic email scan completed. Found {len(emails)} emails")


@celery_app.task(name="parse_and_verify_document")
def parse_and_verify_document(file_bytes: bytes, email_log_id: Optional[int] = None):
    """Celery task to parse document and trigger verification if PO found."""
    logger.info("Parsing document via Celery task")
    
    try:
        # Extract document data
        from app.services.shivaay_ai import extract_document_data
        result = extract_document_data(file_bytes)
        
        if not result.get("success"):
            logger.error(f"Document parsing failed: {result.get('error')}")
            return
        
        data = result.get("data", {})
        invoice_type = data.get("invoice_type", "invoice").lower()
        
        # Save to database
        from app.database import SessionLocal
        from app.models.invoice_model import Invoice
        from app.models.purchase_order_model import PurchaseOrder
        
        db = SessionLocal()
        try:
            if "invoice" in invoice_type:
                invoice = Invoice(
                    file_path="",  # Will be set if file saved
                    file_name="email_attachment",
                    parsing_status="success",
                    **{k: v for k, v in data.items() if hasattr(Invoice, k)}
                )
                db.add(invoice)
                db.commit()
                logger.info(f"Saved invoice {invoice.id}")
            elif "po" in invoice_type or "purchase_order" in invoice_type:
                po = PurchaseOrder(
                    file_path="",
                    file_name="email_attachment",
                    parsing_status="success",
                    **{k: v for k, v in data.items() if hasattr(PurchaseOrder, k)}
                )
                db.add(po)
                db.commit()
                logger.info(f"Saved PO {po.id}")
        finally:
            db.close()
        
    except Exception as e:
        logger.error(f"Error in parse_and_verify_document task: {str(e)}")

