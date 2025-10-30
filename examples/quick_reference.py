#!/usr/bin/env python3
"""
Shivaay AI - Quick Reference Examples
Copy and paste these examples to get started quickly
"""

# =============================================================================
# SETUP
# =============================================================================

# Install package
# pip install openai==1.54.0

# Set API key
# export SHIVAAY_API_KEY="your-api-key"

from openai import OpenAI
import os
import base64

# Initialize client
client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

# =============================================================================
# EXAMPLE 1: Basic Chat
# =============================================================================

def example_basic_chat():
    """Simple question and answer"""
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


# =============================================================================
# EXAMPLE 2: Invoice Analysis
# =============================================================================

def example_invoice_analysis():
    """Analyze invoice text"""
    invoice_text = """
    Invoice #INV-2024-001
    Date: 10/30/2025
    From: Acme Corp
    Total: $1,250.00
    """

    response = client.chat.completions.create(
        model="shivaay",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at extracting structured data from invoices."
            },
            {
                "role": "user",
                "content": f"Extract vendor, invoice number, date, and total from:\n{invoice_text}"
            }
        ],
        temperature=0.3,
        max_tokens=300
    )
    print(response.choices[0].message.content)


# =============================================================================
# EXAMPLE 3: Image OCR
# =============================================================================

def example_image_ocr(image_path):
    """Extract text from invoice image"""
    # Encode image
    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode('utf-8')

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


# =============================================================================
# EXAMPLE 4: Structured Data Extraction
# =============================================================================

def example_structured_extraction():
    """Extract data in JSON format"""
    response = client.chat.completions.create(
        model="shivaay",
        messages=[
            {
                "role": "system",
                "content": "Extract invoice data and return as JSON."
            },
            {
                "role": "user",
                "content": """
Extract these fields in JSON format:
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
    data = json.loads(response.choices[0].message.content)
    print(data)


# =============================================================================
# EXAMPLE 5: Multi-turn Conversation
# =============================================================================

def example_conversation():
    """Have a conversation with context"""
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

    print("User: What is invoice matching?")
    print(f"Assistant: {response1.choices[0].message.content}")

    # Continue conversation
    messages.append({
        "role": "assistant",
        "content": response1.choices[0].message.content
    })
    messages.append({
        "role": "user",
        "content": "What fields should match?"
    })

    response2 = client.chat.completions.create(
        model="shivaay",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

    print("\nUser: What fields should match?")
    print(f"Assistant: {response2.choices[0].message.content}")


# =============================================================================
# EXAMPLE 6: Error Handling
# =============================================================================

def example_with_error_handling():
    """Call API with proper error handling"""
    from openai import OpenAIError, AuthenticationError, RateLimitError

    try:
        response = client.chat.completions.create(
            model="shivaay",
            messages=[
                {"role": "user", "content": "Hello!"}
            ]
        )
        print(response.choices[0].message.content)

    except AuthenticationError:
        print("Invalid API key")
    except RateLimitError:
        print("Rate limit exceeded")
    except OpenAIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# =============================================================================
# EXAMPLE 7: Use in Futurix AI Project
# =============================================================================

def example_futurix_integration():
    """How it's used in the Futurix AI project"""
    from src.services.ocr_service import perform_ocr_with_shivaay

    # The OCR service now uses OpenAI client internally
    image_path = "path/to/invoice.png"
    text, confidence, raw_data = perform_ocr_with_shivaay(image_path)

    print(f"Extracted Text: {text}")
    print(f"Confidence: {confidence}")


# =============================================================================
# MAIN - Run Examples
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  SHIVAAY AI - QUICK REFERENCE EXAMPLES")
    print("=" * 60)

    # Check API key
    if not os.getenv("SHIVAAY_API_KEY"):
        print("\n⚠️  Set SHIVAAY_API_KEY environment variable first!")
        print("   export SHIVAAY_API_KEY='your-api-key'\n")
        exit(1)

    # Uncomment the examples you want to run:

    # example_basic_chat()
    # example_invoice_analysis()
    # example_image_ocr("path/to/image.png")
    # example_structured_extraction()
    # example_conversation()
    # example_with_error_handling()

    print("\n✅ Examples ready to use!")
    print("   Uncomment the functions in main() to run them.\n")

