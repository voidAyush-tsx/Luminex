# Futurix AI - Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Gmail Integration Setup](#gmail-integration-setup)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- poppler-utils (for PDF processing)

### macOS Setup
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install poppler
brew install poppler

# Clone/navigate to project
cd TeamF12

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

### Linux (Ubuntu/Debian) Setup
```bash
# Update package list
sudo apt-get update

# Install Python and poppler
sudo apt-get install -y python3 python3-pip python3-venv poppler-utils

# Navigate to project
cd TeamF12

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

### Windows Setup
```powershell
# Install Python from python.org (3.8+)

# Download poppler for Windows
# https://github.com/oschwartz10612/poppler-windows/releases/
# Extract and add to PATH

# Navigate to project
cd TeamF12

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

### Quick Start Script
```bash
# Make script executable
chmod +x start.sh

# Run the script
./start.sh
```

---

## Docker Deployment

### Build and Run with Docker

```bash
# Build Docker image
docker build -t futurix-ai .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/exports:/app/exports \
  --name futurix-backend \
  futurix-ai

# Check logs
docker logs -f futurix-backend

# Stop container
docker stop futurix-backend

# Remove container
docker rm futurix-backend
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

---

## Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### Systemd Service (Linux)

Create `/etc/systemd/system/futurix.service`:

```ini
[Unit]
Description=Futurix AI Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/futurix
Environment="PATH=/var/www/futurix/venv/bin"
ExecStart=/var/www/futurix/venv/bin/gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable futurix
sudo systemctl start futurix
sudo systemctl status futurix
```

### Nginx Reverse Proxy

Create `/etc/nginx/sites-available/futurix`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/futurix /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Gmail Integration Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "Futurix-Gmail")
3. Note the Project ID

### Step 2: Enable Gmail API

1. Navigate to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Enable"

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Configure OAuth consent screen:
   - User Type: External
   - App name: Futurix AI
   - User support email: your@email.com
   - Scopes: Add Gmail readonly scope
4. Create OAuth client ID:
   - Application type: Desktop app
   - Name: Futurix Gmail Client
5. Download credentials JSON

### Step 4: Setup in Application

```bash
# Copy credentials to project root
cp ~/Downloads/client_secret_*.json ./credentials.json

# Test Gmail connection
python gmail_auto.py test

# Browser will open for authentication
# Grant permissions

# Token will be saved as token.pickle
```

### Step 5: Run Gmail Automation

```bash
# Process emails from last 7 days
python gmail_auto.py

# Or customize search query
# Edit gmail_auto.py and modify GMAIL_SEARCH_QUERY
```

---

## Environment Variables

Create `.env` file (optional):

```env
# Application
APP_NAME="Futurix AI"
APP_VERSION="1.0.0"
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# OCR Settings
OCR_LANGUAGE=en
OCR_DPI=300

# Comparison Settings
VENDOR_FUZZY_THRESHOLD=85
AMOUNT_TOLERANCE_PERCENT=0.5
DATE_TOLERANCE_DAYS=3

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads
EXPORT_DIR=exports

# Gmail
GMAIL_ENABLED=True
GMAIL_MAX_RESULTS=20
```

Load in application:
```python
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv('PORT', 8000))
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

## Cloud Deployment

### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 22.04)
# Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv poppler-utils nginx

# Clone/upload project
git clone https://github.com/your-repo/futurix-ai.git
cd futurix-ai

# Setup and run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Run with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Google Cloud Platform (Cloud Run)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Build and push container
gcloud builds submit --tag gcr.io/PROJECT_ID/futurix-ai

# Deploy to Cloud Run
gcloud run deploy futurix-ai \
  --image gcr.io/PROJECT_ID/futurix-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --max-instances 10
```

### Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create futurix-ai

# Add buildpacks
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
heroku buildpacks:add --index 2 heroku/python

# Create Aptfile for poppler
echo "poppler-utils" > Aptfile

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Performance Optimization

### 1. Caching OCR Results

```python
# Add caching to avoid reprocessing same files
import hashlib
import pickle

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

# Cache OCR results
cache_dir = 'cache'
file_hash = get_file_hash(filepath)
cache_file = f"{cache_dir}/{file_hash}.pkl"

if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        return pickle.load(f)
```

### 2. Background Processing

```python
# Use Celery for background tasks
from celery import Celery

celery = Celery('futurix', broker='redis://localhost:6379')

@celery.task
def process_files_async(invoice_path, po_path):
    # Process in background
    pass
```

### 3. Database Storage

```python
# Use PostgreSQL instead of in-memory storage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:pass@localhost/futurix')
Session = sessionmaker(bind=engine)
```

---

## Monitoring and Logging

### Setup Logging

```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Check Endpoint

Already implemented at `GET /`

### Monitoring with Prometheus

```python
# Install prometheus_client
pip install prometheus-client

# Add metrics
from prometheus_client import Counter, Histogram

upload_counter = Counter('upload_requests_total', 'Total uploads')
processing_time = Histogram('processing_seconds', 'Processing time')
```

---

## Backup and Recovery

### Backup Transactions

```bash
# Backup exports directory
tar -czf backups/exports_$(date +%Y%m%d).tar.gz exports/

# Automated daily backup (cron)
0 0 * * * cd /path/to/futurix && tar -czf backups/exports_$(date +\%Y\%m\%d).tar.gz exports/
```

### Database Backup (if using PostgreSQL)

```bash
# Backup
pg_dump futurix > backups/futurix_$(date +%Y%m%d).sql

# Restore
psql futurix < backups/futurix_20251030.sql
```

---

## Security Best Practices

1. **API Authentication:**
   ```python
   from fastapi.security import APIKeyHeader
   
   api_key_header = APIKeyHeader(name="X-API-Key")
   
   @app.post("/upload")
   async def upload(api_key: str = Depends(api_key_header)):
       if api_key != "your-secret-key":
           raise HTTPException(status_code=403)
   ```

2. **Rate Limiting:**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/upload")
   @limiter.limit("10/minute")
   async def upload(...):
       pass
   ```

3. **File Validation:**
   - Validate file types
   - Check file size
   - Scan for malware

4. **HTTPS Only:**
   - Use SSL/TLS certificates
   - Redirect HTTP to HTTPS

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'paddleocr'"
```bash
pip install paddleocr paddlepaddle
```

### "FileNotFoundError: poppler not found"
```bash
# macOS
brew install poppler

# Ubuntu
sudo apt-get install poppler-utils
```

### "Port 8000 already in use"
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### "Gmail API authentication failed"
```bash
# Delete old token
rm token.pickle

# Re-authenticate
python gmail_auto.py test
```

---

## Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Clean Up Old Files
```bash
# Delete files older than 7 days
find uploads -type f -mtime +7 -delete
find exports -type f -mtime +30 -delete
```

### Monitor Disk Space
```bash
df -h
du -sh uploads/ exports/
```

---

For more information, see:
- [README.md](README.md) - Project overview
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference

