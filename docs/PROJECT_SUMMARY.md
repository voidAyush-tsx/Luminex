# Futurix AI - Project Summary

## 🎯 Project Overview

Futurix AI is a FastAPI backend MVP for AI-powered invoice and purchase order verification. It uses Shivaay AI Vision for OCR, compares extracted fields with fuzzy and tolerant logic, and exports results to CSV.

### Project Type
- ✅ Python FastAPI backend
- ✅ Shivaay AI Vision integration
- ✅ RESTful API architecture
- ✅ HTML/JavaScript frontend (optional)
- ✅ Gmail automation (optional)

---

## 📁 Clean File Structure (Current)

```
TeamF12/
├── src/
│   ├── api/
│   │   └── main.py                  # FastAPI app & API routes
│   ├── core/
│   │   ├── config.py               # App settings (paths, thresholds)
│   │   ├── comparison.py           # Discrepancy detection engine
│   │   └── storage.py              # In-memory storage + CSV export
│   ├── services/
│   │   ├── ocr_service.py          # Shivaay AI OCR integration
│   │   └── gmail_service.py        # Gmail automation (optional)
│   └── utils/
│       └── file_utils.py           # Common file helpers
│
├── data/
│   ├── uploads/                    # Uploaded files (temp)
│   ├── exports/                    # Generated CSV files
│   └── samples/                    # Sample/test files
│
├── public/
│   └── index.html                  # Simple web UI for testing
│
├── scripts/
│   ├── generate_samples.py         # Create sample invoice/PO images
│   └── verify_installation.py      # Environment verification
│
├── tests/
│   └── test_api.py                 # API test helper
│
├── docs/
│   ├── API_DOCUMENTATION.md        # API reference
│   ├── DEPLOYMENT.md               # Deployment guide
│   ├── QUICKSTART.md               # Quick start
│   └── SHIVAAY_AI_SETUP.md         # Shivaay API setup
│
├── run.py                          # Entry point (uvicorn wrapper)
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container build (uses src.api.main)
└── docker-compose.yml              # Local container run
```

---

## ✅ Features

1) File Upload & Preprocessing
- Endpoint: POST /upload
- Accepts: PDF, PNG, JPG, JPEG
- PDF → PNG conversion using pdf2image (first page)

2) OCR-Based Data Extraction (Shivaay AI)
- Extracts: vendor, invoice/po number, date, total, raw text
- Returns an average confidence proxy (fixed 0.90 for AI)

3) Discrepancy Detection
- Vendor: Fuzzy match (threshold 85%)
- Total: 0.5% tolerance
- Date: ±3 days

4) Data Storage & CSV Export
- In-memory transaction list
- GET /export returns CSV with key columns

5) Bonus (Optional)
- Gmail automation service (scripts to be wired by user)
- Web UI page for quick tests (public/index.html)

---

## 🛠 Technology Stack
- FastAPI, Uvicorn, python-multipart
- Shivaay AI Vision via OpenAI-compatible API (requests)
- pdf2image, Pillow
- fuzzywuzzy
- pandas
- google-api-python-client (optional)

---

## 📡 API Endpoints
- GET /           → Health check
- POST /upload    → Upload invoice + PO, extract, compare, store
- GET /export     → Download CSV of transactions
- GET /history    → Recent transactions
- GET /stats      → Stats summary
- DELETE /reset   → Clear all in-memory transactions

---

## 🚀 Run & Test

Prerequisites
- Python 3.8+
- Poppler (for pdf2image)
- Shivaay API key (see docs/SHIVAAY_AI_SETUP.md)

Setup
```bash
pip install -r requirements.txt
export SHIVAAY_API_KEY="<your-key>"
```

Run the server
```bash
python run.py
# or
uvicorn src.api.main:app --reload
```

Open docs
```bash
open http://127.0.0.1:8000/docs
```

Quick upload test (replace files as needed)
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "invoice=@data/samples/test_invoice.png" \
  -F "po=@data/samples/test_po.png"
```

Export CSV
```bash
curl -X GET "http://127.0.0.1:8000/export" -o results.csv
```

Web UI
- Open public/index.html in a browser while the API is running

---

## 🧪 Testing Aids

Generate sample files
```bash
python scripts/generate_samples.py
```

Minimal API test helper
```bash
python tests/test_api.py data/samples/test_invoice.png data/samples/test_po.png
```

Verify environment
```bash
python scripts/verify_installation.py
```

---

## 🔧 Configuration

Key tunables are in `src/core/config.py`:
- Paths: data directories
- OCR model and base URL for Shivaay
- Thresholds: vendor fuzz (85), amount tolerance (0.5%), date tolerance (3)

---

## 📈 Notes & Limits
- In-memory storage resets on server restart
- Only first page of PDF is processed for OCR
- No authentication/rate limiting (MVP)

For production, consider:
- Database (SQLite/Postgres)
- AuthN/AuthZ and rate limiting
- Multi-page PDF handling
- Background tasks for email processing

---

## 🏁 Status
- MVP complete and aligned to the cleaned structure
- Docs and Docker configs updated to use `src.api.main:app`
