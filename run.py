"""
Futurix AI - Invoice & PO Verification System
FastAPI Backend MVP with Shivaay AI Integration
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.main import app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Futurix AI Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

