# 🚀 QUICK START GUIDE - Futurix AI

## 📦 What You Have

A complete **FastAPI backend MVP** for AI-powered invoice and purchase order verification with:
- ✅ OCR-based data extraction (**Shivaay AI Vision**)
- ✅ Smart discrepancy detection
- ✅ CSV export functionality
- ✅ Gmail automation (optional)
- ✅ Web UI included
- ✅ Docker support
- ✅ Full documentation

---

## ⚡ 3-Minute Setup

### Step 0: Get Shivaay AI API Key
Visit **https://shivaay.futurixai.com/playground** and get your API key.

```bash
# Set API key
export SHIVAAY_API_KEY='your-api-key-here'

# Or create config file
echo "your-api-key-here" > shivaay_config.txt
```

### Step 1: Install Dependencies (macOS)
```bash
# Install poppler (required for PDF processing)
brew install poppler

# Navigate to project
cd /Users/HP/WebstormProjects/TeamF12

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
python3 verify_installation.py
```

### Step 3: Start the Server
```bash
# Option A: Using the start script
chmod +x start.sh
./start.sh

# Option B: Direct command
uvicorn main:app --reload
```

### Step 4: Test the API
Open your browser:
- **Interactive API Docs:** http://127.0.0.1:8000/docs
- **Web Interface:** Open `frontend.html` in your browser

---

## 🧪 Quick Test

### Generate Sample Files
```bash
python3 generate_samples.py
```

### Test with Sample Files
```bash
# Using curl
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "invoice=@test_files/test_invoice.png" \
  -F "po=@test_files/test_po.png"

# Using the test script
python3 test_api.py test_files/test_invoice.png test_files/test_po.png
```

### Export Results
```bash
curl -X GET "http://127.0.0.1:8000/export" -o results.csv
```

---

## 📱 Using the Web Interface

1. Start the server: `uvicorn main:app --reload`
2. Open `frontend.html` in your browser
3. Upload invoice and PO files
4. Click "Process Documents"
5. View results and export CSV

---

## 🐳 Docker Alternative

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📧 Gmail Integration (Optional)

### Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download as `credentials.json`
5. Place in project root

### Run
```bash
python3 gmail_auto.py
```

---

## 📚 Documentation

- **README.md** - Project overview
- **API_DOCUMENTATION.md** - Complete API reference
- **DEPLOYMENT.md** - Deployment guides
- **PROJECT_SUMMARY.md** - Detailed project summary

---

## 🆘 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "poppler not found"
```bash
brew install poppler
```

### "Port 8000 already in use"
```bash
uvicorn main:app --port 8001
```

---

## ✅ What Works

- ✅ Upload PDF/PNG/JPG files
- ✅ Extract vendor, amount, date, invoice/PO numbers
- ✅ Compare with fuzzy matching
- ✅ Detect discrepancies
- ✅ Export to CSV
- ✅ View transaction history
- ✅ Get statistics
- ✅ Gmail automation
- ✅ Web interface

---

## 🎯 Next Steps

1. **Test with real invoices:** Upload your own files
2. **Customize settings:** Edit `config.py`
3. **Deploy to cloud:** See `DEPLOYMENT.md`
4. **Add features:** Extend the codebase

---

## 📞 Need Help?

Check these files:
- `README.md` - Detailed setup
- `API_DOCUMENTATION.md` - API usage
- `DEPLOYMENT.md` - Deployment options

---

**🎉 You're all set! Start the server and test the API.**

```bash
uvicorn main:app --reload
# Then open: http://127.0.0.1:8000/docs
```

