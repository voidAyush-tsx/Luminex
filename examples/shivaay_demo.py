"""
Shivaay AI Integration Demo
Demonstrates how to use Shivaay AI with OpenAI-compatible API
"""

import os
from openai import OpenAI


def demo_basic_chat():
    """Basic chat completion example"""
    print("=" * 60)
    print("  DEMO 1: Basic Chat Completion")
    print("=" * 60)

    # Initialize OpenAI client with Shivaay AI endpoint
    client = OpenAI(
        api_key=os.getenv("SHIVAAY_API_KEY", "your-api-key"),
        base_url="https://api.futurixai.com/api/shivaay/v1"
    )

    # Create chat completion
    response = client.chat.completions.create(
        model="shivaay",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        temperature=0.7,
        max_tokens=150
    )

    print("\n📝 Response:")
    print(response.choices[0].message.content)
    print("\n✅ Demo 1 complete!\n")


def demo_invoice_analysis():
    """Invoice analysis example"""
    print("=" * 60)
    print("  DEMO 2: Invoice Analysis")
    print("=" * 60)

    client = OpenAI(
        api_key=os.getenv("SHIVAAY_API_KEY", "your-api-key"),
        base_url="https://api.futurixai.com/api/shivaay/v1"
    )

    response = client.chat.completions.create(
        model="shivaay",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in financial document analysis."
            },
            {
                "role": "user",
                "content": """Analyze this invoice text and extract key information:

Invoice #INV-2024-001
Date: 10/30/2025
From: Acme Corp
Total: $1,250.00

Please provide a structured summary."""
            }
        ],
        temperature=0.3,
        max_tokens=300
    )

    print("\n📊 Analysis:")
    print(response.choices[0].message.content)
    print("\n✅ Demo 2 complete!\n")


def demo_with_conversation():
    """Multi-turn conversation example"""
    print("=" * 60)
    print("  DEMO 3: Multi-turn Conversation")
    print("=" * 60)

    client = OpenAI(
        api_key=os.getenv("SHIVAAY_API_KEY", "your-api-key"),
        base_url="https://api.futurixai.com/api/shivaay/v1"
    )

    # Build conversation
    messages = [
        {"role": "system", "content": "You are a friendly AI assistant."},
        {"role": "user", "content": "Tell me about invoice verification."}
    ]

    # First response
    response1 = client.chat.completions.create(
        model="shivaay",
        messages=messages,
        temperature=0.7,
        max_tokens=200
    )

    print("\n🤖 Assistant:")
    print(response1.choices[0].message.content)

    # Add to conversation
    messages.append({
        "role": "assistant",
        "content": response1.choices[0].message.content
    })
    messages.append({
        "role": "user",
        "content": "What are common discrepancies to check?"
    })

    # Second response
    response2 = client.chat.completions.create(
        model="shivaay",
        messages=messages,
        temperature=0.7,
        max_tokens=200
    )

    print("\n🤖 Assistant:")
    print(response2.choices[0].message.content)
    print("\n✅ Demo 3 complete!\n")


def demo_vision_ocr(image_path=None):
    """Vision-based OCR example"""
    print("=" * 60)
    print("  DEMO 4: Vision OCR (Image Analysis)")
    print("=" * 60)

    if not image_path:
        print("\n⚠️  No image provided. Skipping vision demo.")
        print("   Usage: Provide path to invoice/PO image")
        return

    import base64

    client = OpenAI(
        api_key=os.getenv("SHIVAAY_API_KEY", "your-api-key"),
        base_url="https://api.futurixai.com/api/shivaay/v1"
    )

    # Encode image
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Analyze image
    response = client.chat.completions.create(
        model="shivaay",
        messages=[
            {
                "role": "system",
                "content": "You are an expert document OCR assistant."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all text from this document and identify key fields like vendor, amount, and date."
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

    print(f"\n📄 Image: {image_path}")
    print("\n📝 Extracted Data:")
    print(response.choices[0].message.content)
    print("\n✅ Demo 4 complete!\n")


def main():
    """Run all demos"""
    print("\n" + "🚀" * 30)
    print("  SHIVAAY AI - INTEGRATION DEMO")
    print("🚀" * 30)

    # Check API key
    api_key = os.getenv("SHIVAAY_API_KEY")
    if not api_key or api_key == "your-api-key":
        print("\n⚠️  WARNING: SHIVAAY_API_KEY not set!")
        print("   Set your API key: export SHIVAAY_API_KEY='your-actual-key'")
        print("   Some demos will fail without a valid API key.\n")

    try:
        # Run demos
        demo_basic_chat()
        demo_invoice_analysis()
        demo_with_conversation()

        # Check for image files
        import sys
        if len(sys.argv) > 1:
            demo_vision_ocr(sys.argv[1])
        else:
            # Try to find test images
            test_image = "/Users/HP/WebstormProjects/TeamF12/test_files/test_invoice.png"
            if os.path.exists(test_image):
                demo_vision_ocr(test_image)
            else:
                demo_vision_ocr()

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("   Make sure SHIVAAY_API_KEY is set correctly.")

    print("\n" + "=" * 60)
    print("  ALL DEMOS COMPLETE!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

