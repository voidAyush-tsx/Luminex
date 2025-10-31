# Test Checklist - Futurix AI Backend

## Prerequisites Verification

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `.env.example` with valid credentials
- [ ] Redis running (if using Celery) or in-memory broker configured

## Setup Commands

### 1. Create and Activate Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env and fill in:
# - SHIVAAY_API_KEY
# - GMAIL_CLIENT_ID
# - GMAIL_CLIENT_SECRET
# - GMAIL_REFRESH_TOKEN
# - JWT_SECRET_KEY
```

### 4. Initialize Database (SQLite default)

Database tables are created automatically on first run. For manual creation:

```bash
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

## Running Services

### Start FastAPI Server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected:** Server starts on http://127.0.0.1:8000

### Start Celery Worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

**Expected:** Worker starts and shows "ready" message

### Start Celery Beat

```bash
celery -A app.core.celery_app beat --loglevel=info
```

**Expected:** Beat scheduler starts

## Test Commands

### Health Check

```bash
curl http://127.0.0.1:8000/
```

**Expected:** JSON response with app name, version, status, and database connection

### Run Unit Tests

```bash
pytest -q
```

**Expected:** All tests pass

### Upload Invoice

```bash
curl -X POST "http://127.0.0.1:8000/invoices/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/invoice.pdf"
```

**Expected:** Returns invoice object with ID and parsing_status

### Upload Purchase Order

```bash
curl -X POST "http://127.0.0.1:8000/purchase-orders/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/po.pdf"
```

**Expected:** Returns PO object with ID and parsing_status

### List Invoices

```bash
curl http://127.0.0.1:8000/invoices/
```

**Expected:** JSON array of invoice objects

### List Purchase Orders

```bash
curl http://127.0.0.1:8000/purchase-orders/
```

**Expected:** JSON array of PO objects

### Verify Documents

```bash
curl -X POST "http://127.0.0.1:8000/verify/" \
  -H "Content-Type: application/json" \
  -d '{"invoice_id": 1, "purchase_order_id": 1}'
```

**Expected:** Returns verification result with overall_status and field_checks

### List Verification Results

```bash
curl http://127.0.0.1:8000/verify/
```

**Expected:** JSON array of verification results

### Export All Results to CSV

```bash
curl -O "http://127.0.0.1:8000/export/all"
```

**Expected:** Downloads CSV file with verification results

### Export Verified Only

```bash
curl -O "http://127.0.0.1:8000/export/verified"
```

**Expected:** Downloads CSV with only matched results

### Export Mismatched Only

```bash
curl -O "http://127.0.0.1:8000/export/mismatched"
```

**Expected:** Downloads CSV with only mismatched results

### Trigger Email Sync

```bash
curl -X POST "http://127.0.0.1:8000/email/sync"
```

**Expected:** Returns sync response with emails_found count

## Frontend Integration

### Run Frontend with API Base URL

From `/frontend` directory:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

**Expected:** Frontend connects to backend API

## Common Issues Checklist

### 401 from Shivaay API
- [ ] Verify `SHIVAAY_API_KEY` is correct in `.env`
- [ ] Check API key has not expired
- [ ] Ensure base URL is correct

### Gmail OAuth Issues
- [ ] Verify `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET` are correct
- [ ] Ensure `GMAIL_REFRESH_TOKEN` is valid
- [ ] Check Gmail API scopes

### Celery Broker Issues
- [ ] Redis running: `redis-cli ping` (should return PONG)
- [ ] Check `CELERY_BROKER_URL` in `.env`
- [ ] Verify worker can connect to broker

### Database Connection Errors
- [ ] Verify `DATABASE_URL` in `.env`
- [ ] For SQLite, check file permissions
- [ ] For PostgreSQL, ensure database exists and server is running

### Permission Errors
- [ ] Check `data/uploads` and `data/exports` directories exist
- [ ] Verify write permissions on directories

## Postgres Setup (Optional)

### Switch to PostgreSQL

1. Install PostgreSQL and create database:
```bash
createdb futurix_db
```

2. Update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/futurix_db
```

3. Restart all services

## Docker Testing

### Start with Docker Compose

```bash
docker-compose up -d
```

**Expected:** All services start (redis, api, celery_worker, celery_beat)

### Check Logs

```bash
docker-compose logs -f api
docker-compose logs -f celery_worker
```

### Stop Services

```bash
docker-compose down
```

## Verification Checklist

- [ ] Health endpoint returns healthy status
- [ ] Can upload and parse invoices
- [ ] Can upload and parse purchase orders
- [ ] Verification comparison works correctly
- [ ] CSV exports generate successfully
- [ ] Email sync endpoint responds (may require valid Gmail credentials)
- [ ] Celery tasks execute (check worker logs)
- [ ] Database persists data correctly
- [ ] API documentation accessible at /docs
- [ ] CORS configured for frontend origin

