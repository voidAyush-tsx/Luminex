# 📁 Futurix AI - Project Structure

## 🎯 Clean & Organized Structure

```
TeamF12/
│
├── 📂 src/                          # Source code (organized by function)
│   ├── 📂 api/                      # API layer
│   │   ├── __init__.py
│   │   └── main.py                  # FastAPI app & routes
│   │
│   ├── 📂 core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration settings
│   │   ├── comparison.py            # Comparison engine
│   │   └── storage.py               # Data storage & CSV export
│   │
│   ├── 📂 services/                 # External services integration
│   │   ├── __init__.py
│   │   ├── ocr_service.py           # Shivaay AI OCR service
│   │   └── gmail_service.py         # Gmail API integration
│   │
│   ├── 📂 utils/                    # Utility functions
│   │   ├── __init__.py
│   │   └── file_utils.py            # File handling utilities
│   │
│   └── __init__.py                  # Package initialization
│
├── 📂 data/                         # Data storage
│   ├── 📂 uploads/                  # Uploaded invoice/PO files
│   ├── 📂 exports/                  # Generated CSV exports
│   └── 📂 samples/                  # Sample/test files
│
├── 📂 docs/                         # Documentation
│   ├── README.md                    # Main documentation
│   ├── SHIVAAY_AI_SETUP.md         # Shivaay AI setup guide
│   ├── API_DOCUMENTATION.md         # API reference
│   ├── DEPLOYMENT.md                # Deployment guide
│   ├── PROJECT_SUMMARY.md           # Project overview
│   ├── QUICKSTART.md                # Quick start guide
│   └── COMPLETE_SETUP_GUIDE.md     # Complete setup instructions
│
├── 📂 scripts/                      # Helper scripts
│   ├── generate_samples.py          # Generate test files
│   ├── verify_installation.py       # Verify setup
│   ├── setup_shivaay.sh            # Shivaay AI setup
│   └── create_package.py           # Create ZIP package
│
├── 📂 tests/                        # Test files
│   ├── test_api.py                  # API tests
│   ├── test_ocr.py                  # OCR tests
│   └── test_comparison.py           # Comparison tests
│
├── 📂 public/                       # Public web files
│   └── index.html                   # Web interface
│
├── 📄 run.py                        # Main entry point
├── 📄 requirements.txt              # Python dependencies
├── 📄 .gitignore                   # Git ignore rules
├── 📄 Dockerfile                    # Docker configuration
├── 📄 docker-compose.yml           # Docker Compose setup
└── 📄 README.md                     # Project README
```

---

## 📦 Module Descriptions

### `src/api/` - API Layer
**Purpose:** FastAPI application and HTTP endpoints

**Files:**
- `main.py` - FastAPI app with all routes (/upload, /export, /history, /stats)

**Responsibilities:**
- Handle HTTP requests/responses
- File upload validation
- Route definitions
- CORS configuration

---

### `src/core/` - Core Business Logic
**Purpose:** Core application logic and configuration

**Files:**
- `config.py` - Application settings and configuration
- `comparison.py` - Invoice/PO comparison engine
- `storage.py` - Transaction storage and CSV export

**Responsibilities:**
- Business rules
- Comparison algorithms
- Data storage
- Configuration management

---

### `src/services/` - External Services
**Purpose:** Integration with external APIs and services

**Files:**
- `ocr_service.py` - Shivaay AI OCR integration
- `gmail_service.py` - Gmail API integration

**Responsibilities:**
- Shivaay AI Vision API calls
- Gmail attachment fetching
- External API error handling
- Service authentication

---

### `src/utils/` - Utilities
**Purpose:** Reusable utility functions

**Files:**
- `file_utils.py` - File handling helpers

**Responsibilities:**
- File operations
- Helper functions
- Common utilities

---

### `data/` - Data Storage
**Purpose:** Store all application data

**Subdirectories:**
- `uploads/` - Temporary file storage for uploaded invoices/POs
- `exports/` - Generated CSV export files
- `samples/` - Test and sample files

---

### `docs/` - Documentation
**Purpose:** All project documentation

**Files:**
- `README.md` - Main project documentation
- `SHIVAAY_AI_SETUP.md` - Shivaay AI configuration guide
- `API_DOCUMENTATION.md` - Complete API reference
- `DEPLOYMENT.md` - Deployment instructions
- `PROJECT_SUMMARY.md` - Detailed project overview
- `QUICKSTART.md` - Quick start guide
- `COMPLETE_SETUP_GUIDE.md` - Comprehensive setup instructions

---

### `scripts/` - Helper Scripts
**Purpose:** Development and setup scripts

**Files:**
- `generate_samples.py` - Create test invoice/PO images
- `verify_installation.py` - Check system dependencies
- `setup_shivaay.sh` - Interactive Shivaay AI setup
- `create_package.py` - Package project into ZIP

---

### `tests/` - Test Suite
**Purpose:** Automated tests

**Files:**
- `test_api.py` - API endpoint tests
- `test_ocr.py` - OCR functionality tests
- `test_comparison.py` - Comparison logic tests

---

### `public/` - Web Interface
**Purpose:** Frontend web files

**Files:**
- `index.html` - Interactive web UI for testing

---

## 🚀 How to Use This Structure

### Running the Application

```bash
# From project root
python run.py

# Or directly
uvicorn src.api.main:app --reload
```

### Importing Modules

```python
# Import API
from src.api.main import app

# Import services
from src.services.ocr_service import extract_data_from_file
from src.services.gmail_service import GmailService

# Import core
from src.core.comparison import compare_invoice_po
from src.core.storage import TransactionStorage
from src.core.config import settings

# Import utils
from src.utils.file_utils import save_uploaded_file
```

### Running Scripts

```bash
# Generate test files
python scripts/generate_samples.py

# Verify installation
python scripts/verify_installation.py

# Run tests
python tests/test_api.py
```

---

## 🔧 Configuration

All configuration is centralized in `src/core/config.py`:

```python
from src.core.config import settings

# Access settings
print(settings.UPLOAD_DIR)
print(settings.SHIVAAY_API_BASE)
print(settings.VENDOR_FUZZY_THRESHOLD)
```

---

## 📝 Benefits of This Structure

### ✅ Separation of Concerns
- API logic separate from business logic
- Services isolated from core functionality
- Clear module boundaries

### ✅ Scalability
- Easy to add new services
- Modular components
- Can grow without refactoring

### ✅ Testability
- Each module can be tested independently
- Mock services easily
- Clear dependencies

### ✅ Maintainability
- Easy to locate code
- Logical organization
- Clear naming conventions

### ✅ Professional
- Industry-standard structure
- Follows Python best practices
- Ready for team collaboration

---

## 🎯 Development Workflow

### 1. Adding a New Feature

```
1. Create/update service in src/services/
2. Add business logic in src/core/
3. Create API endpoint in src/api/main.py
4. Add tests in tests/
5. Update documentation in docs/
```

### 2. Modifying Configuration

```
Edit: src/core/config.py
```

### 3. Adding Utilities

```
Add to: src/utils/
```

### 4. Creating Scripts

```
Add to: scripts/
```

---

## 📊 File Count Summary

| Directory | Files | Purpose |
|-----------|-------|---------|
| `src/api/` | 2 | API layer |
| `src/core/` | 4 | Business logic |
| `src/services/` | 3 | External integrations |
| `src/utils/` | 2 | Utilities |
| `data/` | 3 dirs | Data storage |
| `docs/` | 7 | Documentation |
| `scripts/` | 4 | Helper scripts |
| `tests/` | 3 | Test suite |
| `public/` | 1 | Web interface |
| **Root** | 5 | Config & entry point |

**Total: ~34 files + organized directories**

---

## 🔄 Migration from Old Structure

### Old → New Mapping

| Old File | New Location |
|----------|-------------|
| `main.py` | `src/api/main.py` |
| `ocr_utils_shivaay.py` | `src/services/ocr_service.py` |
| `compare_utils.py` | `src/core/comparison.py` |
| `storage.py` | `src/core/storage.py` |
| `config.py` | `src/core/config.py` |
| `gmail_auto.py` | `src/services/gmail_service.py` |
| `test_api.py` | `tests/test_api.py` |
| `generate_samples.py` | `scripts/generate_samples.py` |
| `frontend.html` | `public/index.html` |
| `uploads/` | `data/uploads/` |
| `exports/` | `data/exports/` |
| `*.md` files | `docs/` |

---

## ✅ Best Practices Implemented

1. **Modular Design** - Each module has single responsibility
2. **Clean Imports** - No circular dependencies
3. **Configuration Management** - Centralized settings
4. **Separation of Concerns** - API, Core, Services layers
5. **Testability** - Easy to mock and test
6. **Documentation** - Well-documented code and structure
7. **Scalability** - Easy to extend and maintain

---

**🎉 Your project is now professionally organized and ready for development!**

