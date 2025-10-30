# Shivaay AI Integration Guide

## 🚀 Overview

This project now uses **Shivaay AI** for OCR-based data extraction instead of PaddleOCR. Shivaay AI provides advanced vision AI capabilities through an OpenAI-compatible API.

## 🔑 Getting Your API Key

### Step 1: Visit Shivaay AI Playground
Go to: **https://shivaay.futurixai.com/playground**

### Step 2: Sign up / Log in
Create an account or log in to access your API key

### Step 3: Copy Your API Key
Your API key will be displayed in the playground

## ⚙️ Configuration

You have **3 options** to set your API key:

### Option 1: Environment Variable (Recommended)
```bash
export SHIVAAY_API_KEY='your-api-key-here'
```

For permanent setup, add to your `~/.zshrc` or `~/.bash_profile`:
```bash
echo 'export SHIVAAY_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Option 2: Configuration File
Create a file named `shivaay_config.txt` in the project root:
```bash
echo "your-api-key-here" > shivaay_config.txt
```

**Note:** This file is gitignored for security

### Option 3: Direct Code (Not Recommended)
Edit `ocr_utils_shivaay.py` and set:
```python
SHIVAAY_API_KEY = "your-api-key-here"
```

## 🧪 Testing Your Setup

### 1. Verify API Key is Set
```bash
python3 -c "from ocr_utils_shivaay import get_shivaay_api_key; print('API Key:', get_shivaay_api_key()[:10] + '...')"
```

### 2. Test OCR on Sample File
```bash
# Generate test files first
python3 generate_samples.py

# Test OCR
python3 ocr_utils_shivaay.py test_files/test_invoice.png
```

### 3. Start the Server
```bash
uvicorn main:app --reload
```

### 4. Upload and Process
Visit: http://127.0.0.1:8000/docs

## 📡 Shivaay AI Features Used

### Vision API (GPT-4o)
- **Endpoint:** https://shivaay.futurixai.com/v1/chat/completions
- **Model:** gpt-4o (with vision capabilities)
- **Features:**
  - High-accuracy OCR
  - Structured data extraction
  - Multi-format support (PDF, PNG, JPG)

### OpenAI Compatibility
The API follows OpenAI's format, making it easy to use:
```python
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Extract text from this invoice"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
      ]
    }
  ]
}
```

## 🔍 How It Works

### 1. Image Processing
```
Invoice/PO File → Convert to Base64 → Send to Shivaay AI
```

### 2. Shivaay AI Processing
```
Shivaay AI Vision Model → Analyze Document → Extract Text
```

### 3. Data Extraction
```
Raw Text → Parse Fields → Return Structured Data
```

### Extracted Fields:
- ✅ Vendor/Supplier name
- ✅ Invoice/PO number
- ✅ Date
- ✅ Total amount
- ✅ Complete raw text

## 📊 Advantages of Shivaay AI

### vs PaddleOCR:
1. **Better Accuracy** - AI-powered understanding of document context
2. **Easier Setup** - No heavy ML dependencies
3. **Cloud-Based** - No local model downloads
4. **Faster Processing** - Optimized cloud infrastructure
5. **Structured Output** - Better field recognition

## 💰 Pricing

Check current pricing at: **https://shivaay.futurixai.com**

## 📚 Documentation

- **Main Site:** https://shivaay.futurixai.com
- **API Docs:** https://shivaay.futurixai.com/documentation
- **Playground:** https://shivaay.futurixai.com/playground

## 🔒 Security

### API Key Protection:
- ✅ Never commit API keys to git (`.gitignore` configured)
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Use different keys for dev/prod

### Gitignored Files:
- `shivaay_config.txt` - API key storage
- `.env` - Environment variables

## 🐛 Troubleshooting

### "Shivaay API key not configured"
**Solution:**
```bash
export SHIVAAY_API_KEY='your-key'
# Or create shivaay_config.txt with your key
```

### "Shivaay AI API error: 401"
**Cause:** Invalid or missing API key
**Solution:** Verify your API key at https://shivaay.futurixai.com/playground

### "Shivaay AI API error: 429"
**Cause:** Rate limit exceeded
**Solution:** Wait a moment or upgrade your plan

### "No text could be extracted"
**Causes:**
- Poor image quality
- Unsupported format
- Network issues

**Solutions:**
- Use higher resolution images
- Check internet connection
- Verify file format

## 🔄 Migration from PaddleOCR

### What Changed:
1. **Dependencies:**
   - ❌ Removed: `paddleocr`, `paddlepaddle`
   - ✅ Added: `requests` (lightweight)

2. **OCR Module:**
   - Old: `ocr_utils.py` (PaddleOCR)
   - New: `ocr_utils_shivaay.py` (Shivaay AI)

3. **Configuration:**
   - Now requires: `SHIVAAY_API_KEY`

### Benefits:
- **Smaller Install:** ~2GB less disk space
- **Faster Setup:** No ML model downloads
- **Better Results:** AI-powered understanding
- **Cloud Infrastructure:** Scalable and maintained

## 📝 Example Usage

### Python Code:
```python
from ocr_utils_shivaay import extract_data_from_file

# Extract data from invoice
result = extract_data_from_file("invoice.pdf")

print(f"Vendor: {result['vendor']}")
print(f"Total: {result['total']}")
print(f"Date: {result['date']}")
print(f"Confidence: {result['confidence']}")
```

### API Request:
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -F "invoice=@invoice.pdf" \
  -F "po=@purchase_order.pdf"
```

## ✅ Quick Setup Checklist

- [ ] Get API key from https://shivaay.futurixai.com/playground
- [ ] Set `SHIVAAY_API_KEY` environment variable
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test: `python3 ocr_utils_shivaay.py test_files/test_invoice.png`
- [ ] Start server: `uvicorn main:app --reload`
- [ ] Access: http://127.0.0.1:8000/docs

## 🎉 You're Ready!

Your Futurix AI backend now uses **Shivaay AI** for advanced OCR capabilities!

---

**Questions?** Check the documentation at https://shivaay.futurixai.com/documentation

