"""
Gmail Integration Service
Automatically fetch invoices from Gmail and process them
"""

import os
import base64
import pickle
from typing import List, Dict, Any, Optional
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.core.config import settings


class GmailService:
    """Gmail integration for invoice fetching"""

    def __init__(self, credentials_path: str = 'credentials.json'):
        """Initialize Gmail API connection"""
        self.credentials_path = credentials_path
        self.service = None
        self.authenticate()

    def authenticate(self) -> None:
        """Authenticate with Gmail API"""
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"❌ Gmail credentials not found: {self.credentials_path}")
                    return

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, settings.GMAIL_SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        print("✅ Gmail API authenticated")

    def search_emails(self, query: str = None, max_results: int = None) -> List[Dict[str, Any]]:
        """Search for emails matching query"""
        if query is None:
            query = settings.GMAIL_SEARCH_QUERY
        if max_results is None:
            max_results = settings.GMAIL_MAX_RESULTS

        try:
            if not self.service:
                return []

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            print(f"📧 Found {len(messages)} emails matching query")

            return messages

        except HttpError as error:
            print(f"❌ Gmail API error: {error}")
            return []

    def get_email_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get full email details including attachments"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            return message

        except HttpError as error:
            print(f"❌ Error fetching email {message_id}: {error}")
            return None

    def download_attachment(self, message_id: str, attachment_id: str,
                          filename: str, output_dir: str = None) -> Optional[str]:
        """Download email attachment"""
        if output_dir is None:
            output_dir = settings.UPLOAD_DIR

        try:
            attachment = self.service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()

            file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

            os.makedirs(output_dir, exist_ok=True)

            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(file_data)

            print(f"📎 Downloaded: {filename}")

            return filepath

        except HttpError as error:
            print(f"❌ Error downloading attachment: {error}")
            return None

    def fetch_invoice_attachments(self, query: str = None, max_emails: int = None,
                                 output_dir: str = None) -> List[str]:
        """Fetch all invoice attachments from Gmail"""
        if output_dir is None:
            output_dir = settings.UPLOAD_DIR

        downloaded_files = []

        messages = self.search_emails(query, max_emails)

        if not messages:
            print("📭 No emails found")
            return downloaded_files

        for msg in messages:
            message_id = msg['id']
            email = self.get_email_details(message_id)

            if not email:
                continue

            headers = email.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Unknown')

            print(f"\n📧 Email: {subject[:50]}...")

            parts = email.get('payload', {}).get('parts', [])

            for part in parts:
                filename = part.get('filename', '')

                if filename and any(filename.lower().endswith(ext) for ext in ['.pdf', '.png', '.jpg', '.jpeg']):
                    attachment_id = part.get('body', {}).get('attachmentId')

                    if attachment_id:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        unique_filename = f"gmail_{timestamp}_{filename}"

                        filepath = self.download_attachment(
                            message_id, attachment_id, unique_filename, output_dir
                        )

                        if filepath:
                            downloaded_files.append(filepath)

        print(f"\n✅ Downloaded {len(downloaded_files)} attachments")

        return downloaded_files

