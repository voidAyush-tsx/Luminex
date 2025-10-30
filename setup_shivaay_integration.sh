#!/bin/bash

# Shivaay AI Integration Setup Script
# Run this to set up the integration

echo "=========================================="
echo "  Shivaay AI Integration Setup"
echo "=========================================="
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "   ✅ $python_version"
else
    echo "   ❌ Python 3 not found"
    exit 1
fi

# Install OpenAI package
echo ""
echo "2️⃣  Installing/Upgrading OpenAI package..."
echo "   Checking current version..."

# Check if openai is installed and get version
current_version=$(pip3 show openai 2>/dev/null | grep Version | cut -d' ' -f2)
if [ -n "$current_version" ]; then
    echo "   Current version: $current_version"
fi

# Upgrade to latest
pip3 install --upgrade openai >/dev/null 2>&1
if [ $? -eq 0 ]; then
    new_version=$(pip3 show openai | grep Version | cut -d' ' -f2)
    echo "   ✅ OpenAI package installed/upgraded to $new_version"
else
    echo "   ❌ Failed to install OpenAI package"
    echo "   Try manually: pip3 install --upgrade openai"
    exit 1
fi

# Check if API key is set
echo ""
echo "3️⃣  Checking API key..."
if [ -z "$SHIVAAY_API_KEY" ]; then
    echo "   ⚠️  SHIVAAY_API_KEY not set"
    echo ""
    echo "   Please set your API key:"
    echo "   export SHIVAAY_API_KEY='your-api-key-here'"
    echo ""
    echo "   Or add to ~/.zshrc for permanent setup:"
    echo "   echo 'export SHIVAAY_API_KEY=\"your-api-key\"' >> ~/.zshrc"
    echo "   source ~/.zshrc"
else
    echo "   ✅ SHIVAAY_API_KEY is set"
fi

# Run integration test
echo ""
echo "4️⃣  Running integration test..."
python3 test_shivaay_integration.py

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "📚 Next Steps:"
echo "   1. Set API key (if not already set):"
echo "      export SHIVAAY_API_KEY='your-api-key'"
echo ""
echo "   2. Run demos:"
echo "      python3 examples/shivaay_demo.py"
echo ""
echo "   3. Read documentation:"
echo "      cat docs/SHIVAAY_INTEGRATION.md"
echo ""
echo "   4. Use in your code:"
echo "      from openai import OpenAI"
echo "      client = OpenAI(api_key=..., base_url=...)"
echo ""

