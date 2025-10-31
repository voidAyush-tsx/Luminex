# Futurix AI Backend

AI-Powered Invoice & Purchase Order Verification System - FastAPI Backend

## Overview

This backend provides RESTful APIs for:
- Document parsing via Shivaay AI
- Invoice and Purchase Order management
- Automated verification and comparison
- Gmail integration for email automation
- CSV export functionality
- Background task processing with Celery

## Quick Start

### Prerequisites

- Python 3.11+
- Redis (for Celery broker) or use in-memory broker for local dev
- PostgreSQL (optional, SQLite used by default)

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `SHIVAAY_API_KEY`: Your Shivaay AI API key
- `GMAIL_CLIENT_ID`: Gmail OAuth2 client ID
- `GMAIL_CLIENT_SECRET`: Gmail OAuth2 client secret
- `GMAIL_REFRESH_TOKEN`: Gmail refresh token
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `CORS_ORIGIN`: Frontend origin (default: http://localhost:3000)
- `DATABASE_URL`: Database connection string (default: SQLite)

### 4. Initialize Database

The database tables will be created automatically on first run. For manual initialization:

```bash
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

### 5. Run the Application

#### Start FastAPI Server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Server will be available at: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

#### Start Celery Worker

In a separate terminal:

```bash
celery -A app.core.celery_app worker --loglevel=info
```

#### Start Celery Beat (Scheduler)

In another terminal:

```bash
celery -A app.core.celery_app beat --loglevel=info
```

### 6. Run Tests

```bash
pytest -q
```

## Docker Deployment

### Using Docker Compose

```bash
docker-compose up -d
```

This will start:
- Redis (port 6379)
- FastAPI API (port 8000)
- Celery Worker
- Celery Beat

### Build Docker Image

```bash
docker build -t futurix-backend .
```

## API Endpoints

### Health Check
- `GET /` - Health check and app info

### Invoices
- `GET /invoices/` - List all invoices
- `GET /invoices/{id}` - Get invoice by ID
- `POST /invoices/` - Upload and parse invoice
- `DELETE /invoices/{id}` - Delete invoice

### Purchase Orders
- `GET /purchase-orders/` - List all POs
- `GET /purchase-orders/{id}` - Get PO by ID
- `POST /purchase-orders/` - Upload and parse PO
- `DELETE /purchase-orders/{id}` - Delete PO

### Verification
- `GET /verify/` - List all verification results
- `GET /verify/{id}` - Get verification result by ID
- `POST /verify/` - Compare invoice and PO

### Email Automation
- `POST /email/sync` - Trigger manual email sync
- `GET /email/status` - Get email sync status

### CSV Export
- `GET /export/all` - Export all verification results
- `GET /export/verified` - Export matched results only
- `GET /export/mismatched` - Export mismatched results only

## Testing Examples

### Upload Invoice

```bash
curl -X POST "http://127.0.0.1:8000/invoices/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@invoice.pdf"
```

### Upload Purchase Order

```bash
curl -X POST "http://127.0.0.1:8000/purchase-orders/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@po.pdf"
```

### Verify Documents

```bash
curl -X POST "http://127.0.0.1:8000/verify/" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": 1,
    "purchase_order_id": 1
  }'
```

### Download CSV Export

```bash
curl -O "http://127.0.0.1:8000/export/all"
```

### Trigger Email Sync

```bash
curl -X POST "http://127.0.0.1:8000/email/sync"
```

## Switching to PostgreSQL

1. Install PostgreSQL and create database:
```bash
createdb futurix_db
```

2. Update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/futurix_db
```

3. Restart the application.

## Troubleshooting

### 401 from Shivaay API
- Verify `SHIVAAY_API_KEY` is correct
- Check API key has not expired
- Ensure base URL is correct: `https://api.futurixai.com/api/shivaay/v1`

### Gmail OAuth Issues
- Verify OAuth2 credentials are correct
- Ensure refresh token is valid
- Check Gmail API scopes are configured

### Celery Broker Issues
- Ensure Redis is running: `redis-cli ping`
- Check `CELERY_BROKER_URL` in `.env`
- For local dev without Redis, consider using in-memory broker (not recommended for production)

### Permission Errors on File Upload
- Check `UPLOAD_DIR` and `EXPORT_DIR` directories exist
- Verify write permissions on these directories

### Database Connection Errors
- Verify `DATABASE_URL` is correct
- For PostgreSQL, ensure database exists and credentials are correct
- Check database server is running

## Project Structure

```
backend/
├── app/
│   ├── core/           # Configuration, security, Celery setup
│   ├── models/         # SQLAlchemy database models
│   ├── routers/        # FastAPI route handlers
│   ├── services/       # Business logic services
│   ├── utils/          # Utility functions
│   ├── database.py     # Database connection
│   ├── main.py         # FastAPI app entry point
│   └── schemas.py      # Pydantic schemas
├── tests/              # Unit tests
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose setup
└── README.md          # This file
```

## Development Notes

- All document parsing uses Shivaay AI API (no local OCR)
- Celery tasks run asynchronously for better performance
- Database models use SQLAlchemy with automatic timestamps
- JWT authentication is available but endpoints are public by default
- Logs are stored in `logs/` directory with daily rotation

## License

Proprietary - Futurix AI

