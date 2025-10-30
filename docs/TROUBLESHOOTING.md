# Shivaay AI Integration - Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: `Client.__init__() got an unexpected keyword argument 'proxies'`

**Cause:** Version incompatibility between OpenAI client and httpx library.

**Solution:**

```bash
# Option 1: Upgrade to latest OpenAI
pip uninstall openai
pip install --upgrade openai

# Option 2: Ensure compatible versions
pip install "openai>=1.0.0" "httpx>=0.24.0"

# Option 3: Clean reinstall
pip uninstall openai httpx httpcore -y
pip install openai
```

**Alternative Code Fix:**

If the error persists, use a custom httpx client:

```python
from openai import OpenAI
import httpx

# Create custom httpx client
http_client = httpx.Client(
    timeout=30.0,
    follow_redirects=True
)

# Initialize OpenAI client with custom httpx client
client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.futurixai.com/api/shivaay/v1",
    http_client=http_client
)
```

---

### Issue 2: `SHIVAAY_API_KEY not set`

**Solution:**

```bash
# Temporary (current session only)
export SHIVAAY_API_KEY="your-api-key-here"

# Permanent (add to ~/.zshrc)
echo 'export SHIVAAY_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# Verify
echo $SHIVAAY_API_KEY
```

---

### Issue 3: Import Error - `No module named 'openai'`

**Solution:**

```bash
# Install OpenAI package
pip install openai

# Or install all requirements
pip install -r requirements.txt

# Verify installation
python3 -c "from openai import OpenAI; print('✅ OpenAI installed')"
```

---

### Issue 4: Authentication Error

**Symptoms:**
```
AuthenticationError: Invalid API key
```

**Solution:**

1. Check your API key is correct:
   ```bash
   echo $SHIVAAY_API_KEY
   ```

2. Ensure no extra spaces or quotes:
   ```bash
   # Wrong
   export SHIVAAY_API_KEY=" your-key "  # Has spaces
   
   # Correct
   export SHIVAAY_API_KEY="your-key"
   ```

3. Get a new API key from Futurix AI portal

---

### Issue 5: Connection Error / Timeout

**Symptoms:**
```
APIConnectionError: Connection error
```

**Solution:**

1. Check internet connection
2. Verify the API endpoint is accessible:
   ```bash
   curl -I https://api.futurixai.com/api/shivaay/v1
   ```

3. Increase timeout:
   ```python
   client = OpenAI(
       api_key="your-key",
       base_url="https://api.futurixai.com/api/shivaay/v1",
       timeout=60.0  # Increase to 60 seconds
   )
   ```

---

### Issue 6: Rate Limit Error

**Symptoms:**
```
RateLimitError: Rate limit exceeded
```

**Solution:**

Implement retry logic with exponential backoff:

```python
import time
from openai import OpenAI, RateLimitError

client = OpenAI(
    api_key="your-key",
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

def call_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="shivaay",
                messages=messages
            )
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

---

### Issue 7: Version Conflicts

**Check versions:**

```python
import openai
import httpx

print(f"OpenAI: {openai.__version__}")
print(f"HTTPX: {httpx.__version__}")
```

**Recommended versions:**
- OpenAI: >= 1.0.0
- HTTPX: >= 0.24.0

**Fix:**

```bash
pip install --upgrade openai httpx
```

---

### Issue 8: Image Encoding Issues (Vision API)

**Problem:** Image not being recognized

**Solution:**

Ensure proper base64 encoding:

```python
import base64

def encode_image(image_path):
    """Properly encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Use correct MIME type
import os

ext = os.path.splitext(image_path)[1].lower()
mime_types = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg'
}
mime_type = mime_types.get(ext, 'image/png')

# In your request
{
    "type": "image_url",
    "image_url": {
        "url": f"data:{mime_type};base64,{encode_image(image_path)}"
    }
}
```

---

## Quick Fixes

### Reset Everything

```bash
# Uninstall conflicting packages
pip uninstall openai httpx httpcore -y

# Reinstall fresh
pip install openai

# Test
python3 -c "from openai import OpenAI; print('✅ Working')"
```

### Verify Installation

Run the debug script:

```bash
python3 debug_client.py
```

Or run the test:

```bash
python3 test_openai_client.py
```

---

## Environment Setup Checklist

- [ ] Python 3.7+ installed
- [ ] OpenAI package installed (`pip list | grep openai`)
- [ ] API key set (`echo $SHIVAAY_API_KEY`)
- [ ] No version conflicts
- [ ] Internet connection working
- [ ] Base URL correct: `https://api.futurixai.com/api/shivaay/v1`

---

## Getting Help

If issues persist:

1. Run debug script:
   ```bash
   python3 debug_client.py
   ```

2. Check package versions:
   ```bash
   pip list | grep -E "openai|httpx|httpcore"
   ```

3. Try minimal example:
   ```python
   from openai import OpenAI
   
   client = OpenAI(
       api_key="test",
       base_url="https://api.futurixai.com/api/shivaay/v1"
   )
   print("✅ Client created")
   ```

4. Contact Futurix AI support with:
   - Python version
   - OpenAI package version
   - Error message
   - Stack trace

---

## Working Example (Copy & Paste)

```python
#!/usr/bin/env python3

import os
from openai import OpenAI

# Set API key
# export SHIVAAY_API_KEY="your-key"

client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

try:
    response = client.chat.completions.create(
        model="shivaay",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ],
        temperature=0.7,
        max_tokens=50
    )
    
    print("✅ Success!")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Type: {type(e).__name__}")
```

---

**Last Updated:** October 31, 2025

