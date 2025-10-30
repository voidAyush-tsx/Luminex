# Futurix AI - API Documentation

## Base URL
```
http://127.0.0.1:8000
```

## Interactive Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /`

**Description:** Check if the API is running

**Request:**
```bash
curl http://127.0.0.1:8000/
```

**Response:**
```json
{
  "message": "Futurix AI MVP Backend running 🚀",
  "version": "1.0.0",
  "endpoints": ["/upload", "/export", "/history"]
}
```

---

### 2. Upload and Process Files

**Endpoint:** `POST /upload`

**Description:** Upload invoice and PO files for OCR extraction and comparison

**Content-Type:** `multipart/form-data`

**Parameters:**
- `invoice` (required): Invoice file (PDF/PNG/JPG/JPEG)
- `po` (required): Purchase Order file (PDF/PNG/JPG/JPEG)

**Request Example:**
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "invoice=@invoice.pdf" \
  -F "po=@purchase_order.pdf"
```

**Response Example:**
```json
{
  "status": "processed",
  "invoice": {
    "vendor": "ABC Pvt Ltd",
    "invoice_no": "INV-2025-001",
    "date": "25/10/2025",
    "total": 10000.0,
    "confidence": 0.92,
    "extracted_fields": {
      "vendor": true,
      "total": true,
      "date": true,
      "number": true
    }
  },
  "po": {
    "vendor": "ABC Private Limited",
    "po_no": "PO-2025-001",
    "date": "25/10/2025",
    "total": 9950.0,
    "confidence": 0.89,
    "extracted_fields": {
      "vendor": true,
      "total": true,
      "date": true,
      "number": true
    }
  },
  "result": {
    "status": "MISMATCH ⚠️",
    "matched": false,
    "total_checks": 3,
    "passed_checks": 2,
    "details": {
      "total": {
        "invoice": 10000,
        "po": 9950,
        "difference": 50,
        "difference_percent": "0.50%",
        "reason": "Amount difference exceeds tolerance"
      }
    },
    "summary": {
      "vendor": "✅ Matched",
      "amount": "❌ Mismatch",
      "date": "✅ Matched"
    }
  },
  "transaction_id": 1
}
```

**Status Codes:**
- `200 OK` - Successful processing
- `400 Bad Request` - Invalid file format
- `500 Internal Server Error` - Processing error

---

### 3. Export Transactions to CSV

**Endpoint:** `GET /export`

**Description:** Download all processed transactions as CSV file

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/export" -O
```

**Response:** CSV file download

**CSV Columns:**
- Invoice Vendor
- PO Vendor
- Invoice Total
- PO Total
- Invoice Date
- PO Date
- Invoice Number
- PO Number
- Status
- Mismatched Fields
- Timestamp

**Status Codes:**
- `200 OK` - CSV file returned
- `404 Not Found` - No transactions to export

---

### 4. View Transaction History

**Endpoint:** `GET /history`

**Description:** Get list of recent processed transactions

**Query Parameters:**
- `limit` (optional, default: 10): Number of transactions to return

**Request:**
```bash
curl "http://127.0.0.1:8000/history?limit=5"
```

**Response:**
```json
{
  "total_transactions": 15,
  "showing": 5,
  "transactions": [
    {
      "invoice_vendor": "ABC Pvt Ltd",
      "po_vendor": "ABC Private Limited",
      "invoice_total": 10000,
      "po_total": 9950,
      "invoice_date": "25/10/2025",
      "po_date": "25/10/2025",
      "invoice_number": "INV-2025-001",
      "po_number": "PO-2025-001",
      "status": "MISMATCH ⚠️",
      "timestamp": "2025-10-30 15:23:44",
      "details": {...}
    }
  ]
}
```

---

### 5. Get Processing Statistics

**Endpoint:** `GET /stats`

**Description:** Get overall processing statistics

**Request:**
```bash
curl http://127.0.0.1:8000/stats
```

**Response:**
```json
{
  "total_processed": 25,
  "matched": 18,
  "mismatched": 7,
  "match_rate": "72.00%"
}
```

---

### 6. Reset Storage (Development Only)

**Endpoint:** `DELETE /reset`

**Description:** Clear all stored transactions

**Request:**
```bash
curl -X DELETE http://127.0.0.1:8000/reset
```

**Response:**
```json
{
  "message": "All transactions cleared",
  "total_transactions": 0
}
```

---

## Data Models

### Invoice/PO Extracted Data
```json
{
  "vendor": "string or null",
  "invoice_no": "string or null",
  "po_no": "string or null",
  "date": "string (DD/MM/YYYY) or null",
  "total": "number or null",
  "raw_text": "string",
  "confidence": "number (0-1)",
  "extracted_fields": {
    "vendor": "boolean",
    "total": "boolean",
    "date": "boolean",
    "number": "boolean"
  }
}
```

### Comparison Result
```json
{
  "status": "MATCHED ✅ or MISMATCH ⚠️",
  "matched": "boolean",
  "total_checks": "number",
  "passed_checks": "number",
  "details": {
    "field_name": {
      "invoice": "value",
      "po": "value",
      "difference": "number (optional)",
      "reason": "string"
    }
  },
  "summary": {
    "vendor": "string",
    "amount": "string",
    "date": "string"
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Only .pdf, .png, .jpg, .jpeg files are supported"
}
```

### 404 Not Found
```json
{
  "detail": "No transactions found. Please upload and process files first."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Processing error: <error message>"
}
```

---

## Comparison Logic

### Vendor Matching
- **Method:** Fuzzy string matching using Levenshtein distance
- **Threshold:** 85% similarity
- **Example:** "ABC Pvt Ltd" matches "ABC Private Limited" (similarity > 85%)

### Amount Comparison
- **Method:** Percentage difference from average
- **Tolerance:** 0.5% difference allowed
- **Formula:** `(|amount1 - amount2| / ((amount1 + amount2) / 2)) * 100`
- **Example:** ₹10,000 vs ₹9,950 = 0.50% difference (MATCH)

### Date Comparison
- **Method:** Day difference calculation
- **Tolerance:** ±3 days allowed
- **Example:** 25/10/2025 vs 27/10/2025 = 2 days difference (MATCH)

---

## Field Extraction Patterns

### Vendor
- Patterns: "Vendor:", "Supplier:", "From:", "Company:"
- Fallback: First capitalized line (company name heuristic)

### Amount
- Patterns: "Total:", "Grand Total:", "Amount:", "Net Amount:"
- Currency symbols: ₹, $, €, £
- Format: Supports commas and decimals (e.g., 10,000.50)

### Date
- Patterns: "Date:", "Invoice Date:", "PO Date:"
- Formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, MM/DD/YYYY

### Invoice/PO Number
- Patterns: "Invoice #:", "INV:", "PO #:", "Purchase Order:"
- Format: Alphanumeric with hyphens (e.g., INV-2025-001)

---

## Rate Limiting

Currently no rate limiting (MVP version)

For production, implement:
- Rate limiting per IP
- Request throttling
- API key authentication

---

## CORS Policy

**Current:** Allow all origins (development)

**Headers:**
- Access-Control-Allow-Origin: *
- Access-Control-Allow-Methods: *
- Access-Control-Allow-Headers: *

For production, restrict to specific domains.

---

## File Upload Limits

- **Max file size:** 10 MB (configurable in config.py)
- **Allowed formats:** .pdf, .png, .jpg, .jpeg
- **Storage:** Temporary (files stored in uploads/ directory)

---

## Performance Notes

- **OCR Processing:** ~2-5 seconds per file (depends on file size and quality)
- **PDF Conversion:** ~1-2 seconds per page
- **Comparison:** < 100ms

---

## Testing

### Using curl
```bash
# Test upload
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "invoice=@test_files/test_invoice.png" \
  -F "po=@test_files/test_po.png"

# Test export
curl -X GET "http://127.0.0.1:8000/export" -o export.csv

# Test history
curl "http://127.0.0.1:8000/history?limit=5"
```

### Using Python
```python
import requests

# Upload files
files = {
    'invoice': open('invoice.pdf', 'rb'),
    'po': open('po.pdf', 'rb')
}
response = requests.post('http://127.0.0.1:8000/upload', files=files)
print(response.json())

# Get history
response = requests.get('http://127.0.0.1:8000/history')
print(response.json())
```

---

## Troubleshooting

### "No text extracted from file"
- Check file quality/resolution
- Ensure text is not handwritten
- Try higher DPI for PDF conversion

### "Processing error"
- Check file format is supported
- Verify file is not corrupted
- Check server logs for details

### "Gmail API error"
- Ensure credentials.json is present
- Run authentication: `python gmail_auto.py test`
- Check OAuth consent screen settings

---

For more information, visit the interactive API documentation at http://127.0.0.1:8000/docs

