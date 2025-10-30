"""
Quick Test Script for Shivaay AI Integration
Run this to verify the OpenAI client integration is working
"""

import os
import sys

# Add project root to path
sys.path.insert(0, '/Users/HP/WebstormProjects/TeamF12')

print("=" * 60)
print("  SHIVAAY AI - INTEGRATION TEST")
print("=" * 60)

# Test 1: Check imports
print("\n1️⃣  Testing imports...")
try:
    from openai import OpenAI
    import openai
    print("   ✅ OpenAI client imported successfully")
    # Check version
    if hasattr(openai, '__version__'):
        print(f"   📦 OpenAI version: {openai.__version__}")
    else:
        print("   📦 OpenAI version: (version info not available)")
except ImportError as e:
    print(f"   ❌ Failed to import OpenAI: {e}")
    print("   📦 Install with: pip install openai==1.54.0")
    sys.exit(1)

# Test 2: Check API key
print("\n2️⃣  Checking API key...")
api_key = os.getenv("SHIVAAY_API_KEY")
if api_key and api_key != "your-api-key":
    print(f"   ✅ API key found: {api_key[:8]}...{api_key[-4:]}")
else:
    print("   ⚠️  API key not set or using placeholder")
    print("   Set with: export SHIVAAY_API_KEY='your-actual-key'")

# Test 3: Initialize client
print("\n3️⃣  Initializing Shivaay AI client...")

# Try multiple initialization strategies
client = None
init_success = False

# Strategy 1: Standard initialization
try:
    client = OpenAI(
        api_key=api_key or "test-key",
        base_url="https://api.futurixai.com/api/shivaay/v1"
    )
    print("   ✅ Client initialized successfully")
    print(f"   📍 Base URL: https://api.futurixai.com/api/shivaay/v1")
    init_success = True
except TypeError as e:
    if 'proxies' in str(e):
        print(f"   ⚠️  OpenAI version compatibility issue detected")
        print(f"   Trying workaround...")
        # Strategy 2: Try with explicit timeout only
        try:
            import httpx
            # Create a custom httpx client without proxies
            http_client = httpx.Client(
                base_url="https://api.futurixai.com/api/shivaay/v1",
                timeout=30.0
            )
            client = OpenAI(
                api_key=api_key or "test-key",
                base_url="https://api.futurixai.com/api/shivaay/v1",
                http_client=http_client
            )
            print("   ✅ Client initialized with custom httpx client")
            init_success = True
        except Exception as e2:
            print(f"   ❌ Workaround failed: {e2}")
    else:
        print(f"   ❌ Initialization error: {e}")
except Exception as e:
    print(f"   ❌ Failed to initialize client: {e}")
    print(f"   Error type: {type(e).__name__}")

if not init_success:
    print("\n   💡 Troubleshooting:")
    print("   - Run: python3 debug_client.py (for detailed diagnostics)")
    print("   - Try: pip uninstall openai && pip install --upgrade openai")
    print("   - Check: docs/TROUBLESHOOTING.md")
    print("\n   ⚠️  Continuing with remaining tests...")
    client = None  # Set to None to skip API call test

# Test 4: Test basic call (if API key is valid)
if client and api_key and api_key != "your-api-key":
    print("\n4️⃣  Testing API call...")
    try:
        response = client.chat.completions.create(
            model="shivaay",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello from Shivaay AI!' in one sentence."}
            ],
            temperature=0.7,
            max_tokens=50
        )

        print("   ✅ API call successful!")
        print(f"\n   🤖 Response:")
        print(f"   {response.choices[0].message.content}\n")

    except Exception as e:
        print(f"   ❌ API call failed: {e}")
        print("   Check your API key and internet connection")
elif not client:
    print("\n4️⃣  Skipping API call test (client initialization failed)")
else:
    print("\n4️⃣  Skipping API call test (no valid API key)")

# Test 5: Verify OCR service integration
print("\n5️⃣  Checking OCR service integration...")
try:
    from src.services.ocr_service import perform_ocr_with_shivaay
    from src.core.config import settings

    print("   ✅ OCR service imported successfully")
    print(f"   📊 OCR Model: {settings.OCR_MODEL}")
    print(f"   🔗 API Base: {settings.SHIVAAY_API_BASE}")

except Exception as e:
    print(f"   ❌ Failed to import OCR service: {e}")

# Summary
print("\n" + "=" * 60)
print("  INTEGRATION TEST COMPLETE")
print("=" * 60)

print("\n📚 Next Steps:")
print("   1. Set SHIVAAY_API_KEY environment variable")
print("   2. Run: python examples/shivaay_demo.py")
print("   3. Test with actual images: python examples/shivaay_demo.py path/to/image.png")
print("   4. Use in your app via: from src.services.ocr_service import perform_ocr_with_shivaay")

print("\n💡 Usage Example:")
print("""
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("SHIVAAY_API_KEY"),
    base_url="https://api.futurixai.com/api/shivaay/v1"
)

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
""")

print("\n✨ Done!\n")

