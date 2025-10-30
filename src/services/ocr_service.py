"""
Shivaay AI OCR Service
OCR-based data extraction using Shivaay AI Vision API
"""

import os
import re
import base64
import requests
from typing import Dict, Any, Optional
from datetime import datetime
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path

from src.core.config import settings


def get_shivaay_api_key() -> str:
    """Get Shivaay API key from settings"""
    return settings.get_shivaay_api_key()


def encode_image_to_base64(image_path: str) -> str:
    """
    Encode image to base64 for API submission

    Args:
        image_path: Path to image file

    Returns:
        Base64 encoded image string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def convert_pdf_to_image(pdf_path: str) -> str:
    """
    Convert PDF to image for OCR processing

    Args:
        pdf_path: Path to PDF file

    Returns:
        Path to converted image
    """
    try:
        print(f"📄 Converting PDF to image: {pdf_path}")
        images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=settings.OCR_DPI)

        # Save first page as image
        image_path = pdf_path.replace('.pdf', '_converted.png')
        images[0].save(image_path, 'PNG')

        print(f"✅ Converted to: {image_path}")
        return image_path

    except Exception as e:
        print(f"❌ PDF conversion error: {str(e)}")
        raise Exception(f"Failed to convert PDF: {str(e)}")


def perform_ocr_with_shivaay(image_path: str) -> tuple:
    """
    Perform OCR using Shivaay AI Vision API

    Args:
        image_path: Path to image file

    Returns:
        Tuple of (raw_text, confidence_score, structured_data)
    """
    try:
        print(f"🔍 Running Shivaay AI OCR on: {image_path}")

        api_key = get_shivaay_api_key()
        if not api_key:
            raise Exception("Shivaay API key not configured. Set SHIVAAY_API_KEY environment variable.")

        # Encode image
        base64_image = encode_image_to_base64(image_path)

        # Prepare request to Shivaay AI
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Use OpenAI-compatible chat completion with vision
        payload = {
            "model": settings.OCR_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Extract all text from this invoice or purchase order document.
                            Please extract:
                            1. Vendor/Company name
                            2. Invoice or PO number
                            3. Date
                            4. Total amount
                            5. All other visible text

                            Format the response as:
                            VENDOR: [company name]
                            INVOICE_NO: [invoice number]
                            PO_NO: [PO number if applicable]
                            DATE: [date]
                            TOTAL: [total amount]

                            RAW_TEXT:
                            [all extracted text]
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000
        }

        # Make request to Shivaay AI
        response = requests.post(
            f"{settings.SHIVAAY_API_BASE}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"Shivaay AI API error: {response.status_code} - {response.text}")

        result = response.json()

        # Extract text from response
        if 'choices' in result and len(result['choices']) > 0:
            extracted_text = result['choices'][0]['message']['content']

            # Estimate confidence (Shivaay AI doesn't provide explicit confidence)
            confidence = 0.90  # Default high confidence for AI-based extraction

            print(f"✅ Shivaay AI OCR complete. Confidence: {confidence:.2f}")

            return extracted_text, confidence, result
        else:
            raise Exception("No valid response from Shivaay AI")

    except Exception as e:
        print(f"❌ Shivaay AI OCR error: {str(e)}")
        return "", 0.0, {}


def extract_vendor(text: str) -> Optional[str]:
    """Extract vendor/supplier name from text"""
    # Try to find VENDOR: label from Shivaay AI response
    vendor_match = re.search(r'VENDOR:\s*([^\n]+)', text, re.IGNORECASE)
    if vendor_match:
        vendor = vendor_match.group(1).strip()
        if vendor and vendor.lower() not in ['n/a', 'none', 'not found']:
            return vendor

    # Common patterns for vendor names
    patterns = [
        r'(?:vendor|supplier|from|company|corporation)[:\s]+([A-Za-z0-9\s&.,()-]+?)(?:\n|$)',
        r'([A-Z][A-Za-z\s&.,()-]{5,50})(?:\n|$)',
        r'(?:bill from|sold by)[:\s]+([A-Za-z0-9\s&.,()-]+?)(?:\n|$)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            vendor = match.group(1).strip()
            vendor = re.sub(r'\s+', ' ', vendor)
            if len(vendor) > 3:
                return vendor

    # Fallback: take first capitalized line
    text_lines = text.split('\n')
    for line in text_lines[:10]:
        line = line.strip()
        if len(line) > 5 and line[0].isupper() and any(c.isalpha() for c in line):
            if not re.search(r'\d{4}|\d{1,2}[/-]\d{1,2}', line):
                return line

    return None


def extract_total_amount(text: str) -> Optional[float]:
    """Extract total amount from text"""
    # Try to find TOTAL: label from Shivaay AI response
    total_match = re.search(r'TOTAL:\s*[₹$€£]?\s*([0-9,]+\.?\d*)', text, re.IGNORECASE)
    if total_match:
        amount_str = total_match.group(1).replace(',', '').strip()
        try:
            amount = float(amount_str)
            if 1 <= amount <= 10000000:
                return amount
        except ValueError:
            pass

    # Patterns for total amount
    patterns = [
        r'(?:total|grand total|amount|net amount)[:\s]*[₹$€£]?\s*([0-9,]+\.?\d*)',
        r'[₹$€£]\s*([0-9,]+\.?\d*)\s*(?:total)?',
    ]

    amounts = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            amount_str = match.replace(',', '').strip()
            try:
                amount = float(amount_str)
                if 1 <= amount <= 10000000:
                    amounts.append(amount)
            except ValueError:
                continue

    return max(amounts) if amounts else None


def extract_date(text: str) -> Optional[str]:
    """Extract date from text"""
    # Try to find DATE: label from Shivaay AI response
    date_match = re.search(r'DATE:\s*([^\n]+)', text, re.IGNORECASE)
    if date_match:
        date_str = date_match.group(1).strip()
        if date_str and date_str.lower() not in ['n/a', 'none', 'not found']:
            return date_str

    # Date patterns
    patterns = [
        r'(?:date|dated|invoice date|po date)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            # Normalize date format
            for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%Y-%m-%d', '%d/%m/%y']:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime('%d/%m/%Y')
                except ValueError:
                    continue
            return date_str

    return None


def extract_invoice_number(text: str) -> Optional[str]:
    """Extract invoice number from text"""
    inv_match = re.search(r'INVOICE_NO:\s*([^\n]+)', text, re.IGNORECASE)
    if inv_match:
        inv_no = inv_match.group(1).strip()
        if inv_no and inv_no.lower() not in ['n/a', 'none', 'not found']:
            return inv_no

    patterns = [
        r'(?:invoice|inv|bill)[\s#:]*([A-Z0-9-]+)',
        r'#\s*([A-Z0-9-]{3,})',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            number = match.group(1).strip()
            if len(number) >= 3:
                return number

    return None


def extract_po_number(text: str) -> Optional[str]:
    """Extract PO number from text"""
    po_match = re.search(r'PO_NO:\s*([^\n]+)', text, re.IGNORECASE)
    if po_match:
        po_no = po_match.group(1).strip()
        if po_no and po_no.lower() not in ['n/a', 'none', 'not found']:
            return po_no

    patterns = [
        r'(?:po|purchase order|p\.o\.)[\s#:]*([A-Z0-9-]+)',
        r'(?:order|ref)[\s#:]*([A-Z0-9-]{3,})',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            number = match.group(1).strip()
            if len(number) >= 3:
                return number

    return None


def extract_data_from_file(file_path: str) -> Dict[str, Any]:
    """
    Extract structured data from invoice or PO file using Shivaay AI

    Args:
        file_path: Path to file (PDF or image)

    Returns:
        Dictionary with extracted fields
    """
    try:
        # Convert PDF to image if needed
        if file_path.lower().endswith('.pdf'):
            image_path = convert_pdf_to_image(file_path)
        else:
            image_path = file_path

        # Perform OCR with Shivaay AI
        raw_text, confidence, ocr_results = perform_ocr_with_shivaay(image_path)

        if not raw_text:
            print("⚠️  No text extracted from file")
            return {
                "vendor": None,
                "invoice_no": None,
                "po_no": None,
                "date": None,
                "total": None,
                "raw_text": "",
                "confidence": 0,
                "error": "No text could be extracted",
                "ocr_engine": "Shivaay AI"
            }

        # Extract fields
        vendor = extract_vendor(raw_text)
        total = extract_total_amount(raw_text)
        date = extract_date(raw_text)
        invoice_no = extract_invoice_number(raw_text)
        po_no = extract_po_number(raw_text)

        # Build result
        result = {
            "vendor": vendor,
            "invoice_no": invoice_no,
            "po_no": po_no,
            "date": date,
            "total": total,
            "raw_text": raw_text[:500] + "..." if len(raw_text) > 500 else raw_text,
            "confidence": round(confidence, 2),
            "extracted_fields": {
                "vendor": vendor is not None,
                "total": total is not None,
                "date": date is not None,
                "number": invoice_no is not None or po_no is not None
            },
            "ocr_engine": "Shivaay AI"
        }

        print(f"📊 Extracted: Vendor={vendor}, Total={total}, Date={date}")

        return result

    except Exception as e:
        print(f"❌ Extraction error: {str(e)}")
        return {
            "vendor": None,
            "invoice_no": None,
            "po_no": None,
            "date": None,
            "total": None,
            "raw_text": "",
            "confidence": 0,
            "error": str(e),
            "ocr_engine": "Shivaay AI"
        }

