#!/usr/bin/env python3
"""
Debug script to identify the proxies parameter issue
"""

import sys

print("Checking package versions...")

try:
    import openai
    print(f"✅ openai: {openai.__version__ if hasattr(openai, '__version__') else 'unknown'}")
except:
    print("❌ openai not installed")

try:
    import httpx
    print(f"✅ httpx: {httpx.__version__}")
except:
    print("❌ httpx not installed")

try:
    import httpcore
    print(f"✅ httpcore: {httpcore.__version__}")
except:
    print("❌ httpcore not installed")

print("\nTrying to create OpenAI client...")
try:
    from openai import OpenAI

    # Check the signature of OpenAI.__init__
    import inspect
    sig = inspect.signature(OpenAI.__init__)
    print(f"\nOpenAI.__init__ parameters: {list(sig.parameters.keys())}")

    # Try creating client
    print("\nCreating client...")
    client = OpenAI(
        api_key="test",
        base_url="https://api.futurixai.com/api/shivaay/v1"
    )
    print("✅ Client created successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

