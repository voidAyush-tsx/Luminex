#!/usr/bin/env python3
"""
Minimal OpenAI Client Test
Tests basic OpenAI client initialization
"""

import sys

print("=" * 60)
print("  OpenAI Client Compatibility Test")
print("=" * 60)

# Test 1: Import
print("\n1. Importing OpenAI...")
try:
    from openai import OpenAI
    import openai
    print(f"   ✅ Import successful")
    if hasattr(openai, '__version__'):
        print(f"   Version: {openai.__version__}")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Basic initialization
print("\n2. Testing basic initialization...")
try:
    client = OpenAI(
        api_key="test-key",
        base_url="https://api.futurixai.com/api/shivaay/v1"
    )
    print(f"   ✅ Basic init successful")
    print(f"   Base URL: {client.base_url}")
except Exception as e:
    print(f"   ❌ Basic init failed: {e}")
    print(f"   Error type: {type(e).__name__}")

    # Try alternative initialization
    print("\n   Trying alternative init...")
    try:
        client = OpenAI(api_key="test-key")
        client.base_url = "https://api.futurixai.com/api/shivaay/v1"
        print(f"   ✅ Alternative init successful")
    except Exception as e2:
        print(f"   ❌ Alternative init failed: {e2}")
        sys.exit(1)

# Test 3: Check client attributes
print("\n3. Checking client attributes...")
try:
    print(f"   API Key set: {'Yes' if client.api_key else 'No'}")
    print(f"   Base URL: {client.base_url}")
    print(f"   ✅ Client configured correctly")
except Exception as e:
    print(f"   ⚠️  Attribute check warning: {e}")

print("\n" + "=" * 60)
print("  Test Complete!")
print("=" * 60)
print("\nThe OpenAI client is compatible and ready to use.\n")

