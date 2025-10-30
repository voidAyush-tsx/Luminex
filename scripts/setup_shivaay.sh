#!/bin/bash

# Shivaay AI Setup Script for Futurix AI
# This script helps you configure Shivaay AI for the project

echo "🤖 Shivaay AI Setup for Futurix AI"
echo "===================================="
echo ""

# Check if API key is already set
if [ ! -z "$SHIVAAY_API_KEY" ]; then
    echo "✅ SHIVAAY_API_KEY is already set in environment"
    echo "   API Key: ${SHIVAAY_API_KEY:0:10}..."
    echo ""
    read -p "Do you want to update it? (y/n): " update_key
    if [ "$update_key" != "y" ]; then
        echo "Keeping existing API key."
        exit 0
    fi
fi

# Check for config file
if [ -f "shivaay_config.txt" ]; then
    echo "✅ Found shivaay_config.txt"
    existing_key=$(cat shivaay_config.txt)
    echo "   API Key: ${existing_key:0:10}..."
    echo ""
    read -p "Do you want to update it? (y/n): " update_file
    if [ "$update_file" != "y" ]; then
        echo "Keeping existing config file."
        exit 0
    fi
fi

echo ""
echo "📝 Shivaay AI API Key Setup"
echo "============================"
echo ""
echo "To get your API key:"
echo "  1. Visit: https://shivaay.futurixai.com/playground"
echo "  2. Sign up or log in"
echo "  3. Copy your API key"
echo ""

read -p "Enter your Shivaay AI API key: " api_key

if [ -z "$api_key" ]; then
    echo ""
    echo "❌ No API key provided. Setup cancelled."
    exit 1
fi

echo ""
echo "Choose how to save your API key:"
echo ""
echo "1. Environment variable (current session)"
echo "2. Save to shivaay_config.txt (recommended)"
echo "3. Add to ~/.zshrc (permanent)"
echo "4. Both config file and ~/.zshrc"
echo ""

read -p "Select option (1-4): " option

case $option in
    1)
        export SHIVAAY_API_KEY="$api_key"
        echo ""
        echo "✅ API key set for current session"
        echo "   To make it permanent, add to ~/.zshrc:"
        echo "   export SHIVAAY_API_KEY='$api_key'"
        ;;
    2)
        echo "$api_key" > shivaay_config.txt
        echo ""
        echo "✅ API key saved to shivaay_config.txt"
        echo "   This file is gitignored for security"
        ;;
    3)
        echo "" >> ~/.zshrc
        echo "# Shivaay AI API Key" >> ~/.zshrc
        echo "export SHIVAAY_API_KEY='$api_key'" >> ~/.zshrc
        source ~/.zshrc
        echo ""
        echo "✅ API key added to ~/.zshrc"
        echo "   Restart terminal or run: source ~/.zshrc"
        ;;
    4)
        echo "$api_key" > shivaay_config.txt
        echo "" >> ~/.zshrc
        echo "# Shivaay AI API Key" >> ~/.zshrc
        echo "export SHIVAAY_API_KEY='$api_key'" >> ~/.zshrc
        source ~/.zshrc
        echo ""
        echo "✅ API key saved to:"
        echo "   - shivaay_config.txt"
        echo "   - ~/.zshrc"
        ;;
    *)
        echo ""
        echo "❌ Invalid option. Setup cancelled."
        exit 1
        ;;
esac

echo ""
echo "🧪 Testing Shivaay AI Connection..."
echo ""

# Test the API key
python3 -c "
from ocr_utils_shivaay import get_shivaay_api_key
api_key = get_shivaay_api_key()
if api_key:
    print('✅ API key loaded successfully')
    print(f'   Key: {api_key[:10]}...')
else:
    print('❌ Failed to load API key')
    exit(1)
" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Shivaay AI setup complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Generate test files: python3 generate_samples.py"
    echo "  2. Test OCR: python3 ocr_utils_shivaay.py test_files/test_invoice.png"
    echo "  3. Start server: uvicorn main:app --reload"
    echo ""
else
    echo ""
    echo "⚠️  Setup complete but API key test failed"
    echo "   Please verify your API key at:"
    echo "   https://shivaay.futurixai.com/playground"
    echo ""
fi

