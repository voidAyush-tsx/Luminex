# 🚀 Futurix AI - Invoice & PO Verification System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Shivaay AI](https://img.shields.io/badge/Shivaay_AI-Powered-purple.svg)](https://shivaay.futurixai.com)

> **Professional, production-ready MVP for AI-powered invoice and purchase order verification**

---

## 📁 Clean Project Structure

```
TeamF12/
├── src/              # Source code (organized by function)
│   ├── api/          # FastAPI routes
│   ├── core/         # Business logic
│   ├── services/     # External integrations (Shivaay AI, Gmail)
│   └── utils/        # Utilities
├── data/             # Data storage (uploads, exports, samples)
├── docs/             # Documentation
├── scripts/          # Helper scripts
├── tests/            # Test suite
├── public/           # Web interface
└── run.py            # Main entry point
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete details.

---

## ✨ Features

- ✅ **Shivaay AI Vision** - Advanced AI-powered OCR
- ✅ **Smart Comparison** - Fuzzy matching with configurable tolerance
- ✅ **REST API** - 6 endpoints with interactive docs
- ✅ **CSV Export** - Download verification results
- ✅ **Gmail Integration** - Auto-fetch invoices from email
- ✅ **Web Interface** - Beautiful drag & drop UI
- ✅ **Docker Support** - Containerized deployment
- ✅ **Comprehensive Docs** - API, setup, deployment guides

---

## 🚀 Quick Start (3 Steps)

### 1. Get Shivaay AI API Key
Visit: **https://shivaay.futurixai.com/playground**

```bash
export SHIVAAY_API_KEY='your-api-key-here'
```

### 2. Install Dependencies
```bash
cd TeamF12
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python run.py
# Or: uvicorn src.api.main:app --reload
```

**Access:**
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Web UI: Open `public/index.html`

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/upload` | POST | Upload & process files |
| `/export` | GET | Download CSV |
| `/history` | GET | Transaction history |
| `/stats` | GET | Statistics |
| `/reset` | DELETE | Clear data |

**Full API docs:** [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

---

## 💻 Usage Example

### Python
```python
import requests

# Upload files
files = {
    'invoice': open('invoice.pdf', 'rb'),
    'po': open('po.pdf', 'rb')
}
response = requests.post('http://127.0.0.1:8000/upload', files=files)
print(response.json())
```

### cURL
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "invoice=@invoice.pdf" \
  -F "po=@purchase_order.pdf"
```

### Web Interface
Open `public/index.html` in your browser for drag & drop interface.

---

## 🎯 What Gets Extracted

From each document:
- **Vendor/Company Name** (fuzzy matching)
- **Invoice/PO Number**
- **Date** (multiple formats supported)
- **Total Amount** (with currency symbols)
- **Confidence Score**

---

## ⚖️ Comparison Logic

| Field | Method | Tolerance |
|-------|--------|-----------|
| Vendor | Fuzzy matching | 85% similarity |
| Amount | Percentage diff | 0.5% |
| Date | Day difference | ±3 days |

---

## 📦 Technology Stack

- **Backend:** FastAPI 0.104.1
- **OCR:** Shivaay AI Vision (gpt-4o)
- **Comparison:** FuzzyWuzzy
- **Export:** Pandas
- **Server:** Uvicorn
- **Optional:** Gmail API

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Project organization |
| [docs/SHIVAAY_AI_SETUP.md](docs/SHIVAAY_AI_SETUP.md) | Shivaay AI setup guide |
| [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) | API reference |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deployment guide |
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | Quick start guide |

---

## 🛠️ Development

### Project Structure
```python
# Import modules
from src.api.main import app
from src.services.ocr_service import extract_data_from_file
from src.core.comparison import compare_invoice_po
from src.core.storage import TransactionStorage
from src.core.config import settings
```

### Run Tests
```bash
python tests/test_api.py
```

### Generate Samples
```bash
python scripts/generate_samples.py
```

### Verify Setup
```bash
python scripts/verify_installation.py
```

---

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for more options.

---

## 🔒 Security

- ✅ API keys via environment variables
- ✅ Gitignored config files
- ✅ CORS configuration
- ✅ File validation

---

## 📊 CSV Export Format

11 columns:
1. Invoice Vendor
2. PO Vendor
3. Invoice Total
4. PO Total
5. Invoice Date
6. PO Date
7. Invoice Number
8. PO Number
9. Status (MATCHED ✅ / MISMATCH ⚠️)
10. Mismatched Fields
11. Timestamp

---

## 🎨 Web Interface

Beautiful gradient UI with:
- Drag & drop file upload
- Real-time processing feedback
- Results visualization
- CSV export button
- Mobile responsive

---

## 📧 Gmail Automation

Auto-fetch invoices from email:

```bash
# Setup OAuth credentials
python scripts/setup_shivaay.sh

# Run automation
from src.services.gmail_service import GmailService
gmail = GmailService()
files = gmail.fetch_invoice_attachments()
```

---

## 🆘 Troubleshooting

### "Shivaay API key not configured"
```bash
export SHIVAAY_API_KEY='your-key'
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "poppler not found"
```bash
brew install poppler  # macOS
sudo apt-get install poppler-utils  # Linux
```

---

## 🎓 Learn More

- **Shivaay AI:** https://shivaay.futurixai.com
- **API Docs:** https://shivaay.futurixai.com/documentation
- **Interactive Docs:** http://127.0.0.1:8000/docs

---

## 🤝 Contributing

This is a clean, modular codebase ready for:
- Adding features
- Team collaboration
- Production deployment

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture details.

---

## 📄 License

MIT License - Free to use and modify

---

## 🎉 Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Shivaay AI](https://shivaay.futurixai.com/) - Advanced Vision AI
- [Gmail API](https://developers.google.com/gmail/api)

---

**Futurix AI** - Powered by Shivaay AI 🤖 | Professionally Organized ⭐

**Status:** ✅ Production-Ready MVP | ✅ Clean Architecture | ✅ Fully Documented

