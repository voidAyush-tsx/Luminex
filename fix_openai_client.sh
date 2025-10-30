#!/bin/bash

# Quick fix script for OpenAI client issues

echo "=========================================="
echo "  Shivaay AI - Quick Fix"
echo "=========================================="
echo ""

echo "🔧 Fixing OpenAI client compatibility issue..."
echo ""

# Step 1: Clean uninstall
echo "1️⃣  Removing existing packages..."
pip3 uninstall openai httpx httpcore -y >/dev/null 2>&1
echo "   ✅ Old packages removed"

# Step 2: Fresh install
echo ""
echo "2️⃣  Installing latest compatible versions..."
pip3 install --upgrade openai httpx >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Packages installed successfully"

    # Show versions
    echo ""
    echo "📦 Installed versions:"
    pip3 show openai | grep "Name:\|Version:"
    pip3 show httpx | grep "Name:\|Version:"
else
    echo "   ❌ Installation failed"
    exit 1
fi

# Step 3: Test
echo ""
echo "3️⃣  Testing OpenAI client..."
python3 -c "
from openai import OpenAI
client = OpenAI(
    api_key='test',
    base_url='https://api.futurixai.com/api/shivaay/v1'
)
print('   ✅ Client initialization successful!')
" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  ✅ Fix Applied Successfully!"
    echo "=========================================="
    echo ""
    echo "You can now:"
    echo "  1. Run: python3 test_shivaay_integration.py"
    echo "  2. Run: python3 examples/shivaay_demo.py"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "  ⚠️  Issue Persists"
    echo "=========================================="
    echo ""
    echo "Try manual fix:"
    echo "  pip3 uninstall openai -y"
    echo "  pip3 install openai"
    echo ""
    echo "Or check: docs/TROUBLESHOOTING.md"
    echo ""
fi

