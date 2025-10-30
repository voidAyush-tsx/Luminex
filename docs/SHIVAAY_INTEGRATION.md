# Shivaay AI Integration Guide

Complete guide for integrating Shivaay AI with OpenAI-compatible API in your Python projects.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## 🔍 Overview

Shivaay AI provides an OpenAI-compatible API that can be used with the official OpenAI Python client library. This makes integration seamless and familiar for developers already using OpenAI.

**Key Features:**
- OpenAI-compatible API
- Vision support for document OCR
- Chat completions for text analysis
- Multi-turn conversations
- Structured data extraction

**Base URL:** `https://api.futurixai.com/api/shivaay/v1`

---

## 📦 Installation

### 1. Install Dependencies

```bash
pip install openai
```

Or add to your `requirements.txt`:

```text
openai==1.54.0
```

### 2. Set API Key

Set your Shivaay AI API key as an environment variable:

```bash
export SHIVAAY_API_KEY="your-api-key-here"
```

For permanent setup, add to your `.env` file:

```env
SHIVAAY_API_KEY=your-api-key-here
```

---

## 🚀 Quick Start

### Basic Chat Completion

```python
from openai import OpenAI

# Initialize client
client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

# Create completion
response = client.chat.completions.create(
    model="shivaay",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.7,
    max_tokens=150
)

print(response.choices[0].message.content)
```

---

## 💡 Usage Examples

### Example 1: Simple Question & Answer

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

response = client.chat.completions.create(
    model="shivaay",
    messages=[
        {"role": "system", "content": "You are a financial expert."},
        {"role": "user", "content": "Explain invoice discrepancy detection."}
    ],
    temperature=0.7,
    max_tokens=200
)

print(response.choices[0].message.content)
```

### Example 2: Document Analysis

```python
client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

invoice_text = """
Invoice #INV-2024-001
Date: 10/30/2025
From: Acme Corp
Amount: $1,250.00
"""

response = client.chat.completions.create(
    model="shivaay",
    messages=[
        {
            "role": "system",
            "content": "Extract structured data from invoices."
        },
        {
            "role": "user",
            "content": f"Extract key fields from this invoice:\n\n{invoice_text}"
        }
    ],
    temperature=0.3,
    max_tokens=300
)

print(response.choices[0].message.content)
```

### Example 3: Multi-turn Conversation

```python
client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

# Build conversation history
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is invoice matching?"}
]

# First turn
response1 = client.chat.completions.create(
    model="shivaay",
    messages=messages,
    temperature=0.7,
    max_tokens=150
)

print("Assistant:", response1.choices[0].message.content)

# Continue conversation
messages.append({
    "role": "assistant",
    "content": response1.choices[0].message.content
})
messages.append({
    "role": "user",
    "content": "What fields should match?"
})

# Second turn
response2 = client.chat.completions.create(
    model="shivaay",
    messages=messages,
    temperature=0.7,
    max_tokens=150
)

print("Assistant:", response2.choices[0].message.content)
```

### Example 4: Vision OCR (Image Analysis)

```python
from openai import OpenAI
import base64
import os

client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

# Encode image to base64
with open("invoice.png", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Analyze image
response = client.chat.completions.create(
    model="shivaay",
    messages=[
        {
            "role": "system",
            "content": "You are an expert OCR assistant."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract all text and identify vendor, amount, and date."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    temperature=0.3,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### Example 5: Structured Data Extraction

```python
client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

response = client.chat.completions.create(
    model="shivaay",
    messages=[
        {
            "role": "system",
            "content": "Extract data in JSON format."
        },
        {
            "role": "user",
            "content": """
Extract the following fields in JSON format:
- vendor
- invoice_number
- date
- total

From this text:
Invoice #123
ABC Company
Date: 10/30/2025
Total: $500.00
"""
        }
    ],
    temperature=0.2,
    max_tokens=200
)

import json
extracted_data = json.loads(response.choices[0].message.content)
print(extracted_data)
```

---

## 📚 API Reference

### Client Initialization

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",           # Your Shivaay API key
    base_url="https://api.futurixai.com/api/shivaay/v1"  # Shivaay endpoint
)
```

### Chat Completion Parameters

```python
response = client.chat.completions.create(
    model="shivaay",                  # Model name (required)
    messages=[...],                   # Conversation messages (required)
    temperature=0.7,                  # Randomness (0.0-2.0, default: 1.0)
    max_tokens=150,                   # Max response length
    top_p=1.0,                        # Nucleus sampling
    frequency_penalty=0.0,            # Penalize frequent tokens
    presence_penalty=0.0              # Penalize present tokens
)
```

### Message Format

**Text Message:**
```python
{
    "role": "user|assistant|system",
    "content": "text content"
}
```

**Vision Message (with image):**
```python
{
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Analyze this image"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "data:image/png;base64,{base64_image}"
            }
        }
    ]
}
```

### Response Structure

```python
{
    "id": "chatcmpl-...",
    "object": "chat.completion",
    "created": 1234567890,
    "model": "shivaay",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Response text"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30
    }
}
```

---

## 🛡️ Error Handling

### Basic Error Handling

```python
from openai import OpenAI, OpenAIError

client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

try:
    response = client.chat.completions.create(
        model="shivaay",
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    print(response.choices[0].message.content)
    
except OpenAIError as e:
    print(f"API Error: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

### Handling Common Errors

```python
from openai import (
    OpenAI,
    APIError,
    AuthenticationError,
    RateLimitError,
    APITimeoutError
)

try:
    response = client.chat.completions.create(...)
    
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded, wait before retrying")
except APITimeoutError:
    print("Request timed out")
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

---

## ✨ Best Practices

### 1. Use Environment Variables

```python
import os
from openai import OpenAI

# ✅ Good: Use environment variables
client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

# ❌ Bad: Hardcode API keys
client = OpenAI(
    api_key="sk-1234...",  # Don't do this!
    base_url="https://api.futurixai.com/api/shivaay/v1"
)
```

### 2. Set Appropriate Temperature

```python
# For factual/structured extraction: Low temperature
response = client.chat.completions.create(
    model="shivaay",
    messages=[...],
    temperature=0.2  # More deterministic
)

# For creative tasks: Higher temperature
response = client.chat.completions.create(
    model="shivaay",
    messages=[...],
    temperature=0.8  # More creative
)
```

### 3. Use System Messages

```python
# ✅ Good: Clear system message
response = client.chat.completions.create(
    model="shivaay",
    messages=[
        {
            "role": "system",
            "content": "You are an expert at extracting invoice data. Always return JSON format."
        },
        {"role": "user", "content": "Extract data from..."}
    ]
)
```

### 4. Handle Image Formats Properly

```python
import base64

# Support multiple image formats
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

# Detect format
import os
ext = os.path.splitext(image_path)[1].lower()
mime_type = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg'
}.get(ext, 'image/png')

# Use in request
response = client.chat.completions.create(
    model="shivaay",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{encode_image(image_path)}"
                    }
                }
            ]
        }
    ]
)
```

### 5. Implement Retry Logic

```python
import time
from openai import OpenAI, RateLimitError

def call_shivaay_with_retry(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="shivaay",
                messages=messages
            )
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

---

## 🔧 Integration in Futurix AI Project

The OCR service has been updated to use the OpenAI client:

**File:** `src/services/ocr_service.py`

```python
from openai import OpenAI
from src.core.config import settings

def perform_ocr_with_shivaay(image_path: str) -> tuple:
    """Perform OCR using Shivaay AI Vision API"""
    
    # Initialize client
    client = OpenAI(
        api_key=settings.get_shivaay_api_key(),
        base_url=settings.SHIVAAY_API_BASE
    )
    
    # Encode image
    base64_image = encode_image_to_base64(image_path)
    
    # Call API
    response = client.chat.completions.create(
        model=settings.OCR_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert document analysis assistant."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract invoice data..."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content
```

---

## 📖 Additional Resources

- **Official Documentation:** [Futurix AI Docs](https://api.futurixai.com/docs)
- **OpenAI Python Client:** [GitHub](https://github.com/openai/openai-python)
- **Demo Script:** `examples/shivaay_demo.py`

---

## 🎯 Quick Reference

| Task | Temperature | Max Tokens |
|------|------------|------------|
| Data Extraction | 0.2-0.3 | 500-1000 |
| Classification | 0.1-0.2 | 50-100 |
| Summarization | 0.5-0.7 | 200-500 |
| Creative Writing | 0.8-1.0 | 500+ |
| Q&A | 0.3-0.5 | 100-300 |

---

**Last Updated:** October 30, 2025  
**Version:** 1.0.0

