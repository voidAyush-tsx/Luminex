"""Shivaay AI integration service for document parsing."""

import os
import time
from typing import Dict, Any, Optional
from app.core.config import get_settings
from app.utils.logger import logger
from app.utils.validators import parse_decimal, parse_date, normalize_string

settings = get_settings()

# Initialize client lazily to avoid import errors
_client = None


def get_shivaay_client():
    """Get or create Shivaay AI client."""
    global _client
    if _client is None:
        from openai import OpenAI
        _client = OpenAI(
            api_key=settings.shivaay_api_key,
            base_url=settings.shivaay_base_url
        )
    return _client


def extract_document_data(file_bytes: bytes, max_retries: int = 3, retry_delay: float = 1.0) -> Dict[str, Any]:
    """
    Extract structured data from document using Shivaay AI API.
    
    Args:
        file_bytes: Document file as bytes
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    
    Returns:
        Dictionary with parsed document fields
    """
    client = get_shivaay_client()
    
    prompt = """Extract the following information from this document and return as JSON:
- vendor_name: Name of the vendor/supplier
- vendor_address: Full address of vendor
- invoice_no: Invoice number (if invoice)
- po_no: Purchase order number (if PO)
- date: Document date (ISO format: YYYY-MM-DD)
- due_date: Due date (ISO format: YYYY-MM-DD)
- currency: Currency code (e.g., USD, EUR)
- subtotal: Subtotal amount (numeric)
- tax: Tax amount (numeric)
- total_amount: Total amount (numeric)
- line_items: Array of objects with {description, qty, unit_price}
- taxes: Array of tax details if available
- invoice_type: "invoice" or "po" or "purchase_order"

Return only valid JSON without markdown formatting."""

    for attempt in range(max_retries):
        try:
            logger.info(f"Shivaay AI API call attempt {attempt + 1}/{max_retries}")
            
            # Prepare file for upload - Shivaay API expects base64 encoded data
            import base64
            import json as json_lib
            
            # Encode file bytes to base64
            file_base64 = base64.b64encode(file_bytes).decode('utf-8')
            
            # Use OpenAI-style client with vision model
            # Note: Adjust model name based on Shivaay API documentation
            # For PDFs, Shivaay API may require different handling - check API docs
            # This example uses image format; adjust MIME type as needed
            response = client.chat.completions.create(
                model="gpt-4o",  # Adjust based on Shivaay API model - may be "gpt-4-vision" or custom
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    # Adjust MIME type based on file type (image/png, image/jpeg, application/pdf)
                                    "url": f"data:image/png;base64,{file_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.1,
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            import json
            parsed_data = json.loads(content)
            
            # Normalize and validate fields
            normalized_data = {
                "vendor_name": normalize_string(parsed_data.get("vendor_name")),
                "vendor_address": normalize_string(parsed_data.get("vendor_address")),
                "invoice_no": normalize_string(parsed_data.get("invoice_no")),
                "po_no": normalize_string(parsed_data.get("po_no")),
                "date": parse_date(parsed_data.get("date")),
                "due_date": parse_date(parsed_data.get("due_date")),
                "currency": normalize_string(parsed_data.get("currency", "USD")),
                "subtotal": parse_decimal(parsed_data.get("subtotal")),
                "tax": parse_decimal(parsed_data.get("tax")),
                "total_amount": parse_decimal(parsed_data.get("total_amount")),
                "line_items": parsed_data.get("line_items", []),
                "taxes": parsed_data.get("taxes", []),
                "invoice_type": normalize_string(parsed_data.get("invoice_type", "invoice")),
            }
            
            logger.info("Shivaay AI extraction successful")
            return {
                "success": True,
                "data": normalized_data,
                "raw_response": parsed_data,
            }
            
        except Exception as e:
            logger.error(f"Shivaay AI API error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                continue
            else:
                return {
                    "success": False,
                    "error": str(e),
                    "data": {},
                }
    
    return {
        "success": False,
        "error": "Max retries exceeded",
        "data": {},
    }

