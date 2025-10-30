"""
Futurix AI - Main FastAPI Application
API Routes and Server Configuration
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from datetime import datetime
from typing import Optional

from src.services.ocr_service import extract_data_from_file
from src.core.comparison import compare_invoice_po
from src.core.storage import TransactionStorage, export_to_csv
from src.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Futurix AI - Invoice & PO Verification",
    description="AI-powered invoice and purchase order verification system using Shivaay AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.EXPORT_DIR, exist_ok=True)

# Initialize storage
storage = TransactionStorage()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Futurix AI MVP Backend running 🚀",
        "version": "1.0.0",
        "ocr_engine": "Shivaay AI Vision",
        "endpoints": ["/upload", "/export", "/history", "/stats"],
        "setup_guide": "See docs/SHIVAAY_AI_SETUP.md for API key configuration",
        "status": "operational"
    }


@app.post("/upload")
async def upload_and_process(
    invoice: UploadFile = File(...),
    po: UploadFile = File(...)
):
    """
    Upload invoice and PO files, extract data, and compare

    Args:
        invoice: Invoice file (PDF/PNG/JPG)
        po: Purchase Order file (PDF/PNG/JPG)

    Returns:
        JSON with extracted data and comparison results
    """
    try:
        # Validate file formats
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg'}

        invoice_ext = os.path.splitext(invoice.filename)[1].lower()
        po_ext = os.path.splitext(po.filename)[1].lower()

        if invoice_ext not in allowed_extensions or po_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Only {', '.join(allowed_extensions)} files are supported"
            )

        # Generate unique filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        invoice_filename = f"invoice_{timestamp}{invoice_ext}"
        po_filename = f"po_{timestamp}{po_ext}"

        invoice_path = os.path.join(settings.UPLOAD_DIR, invoice_filename)
        po_path = os.path.join(settings.UPLOAD_DIR, po_filename)

        # Save uploaded files
        with open(invoice_path, "wb") as f:
            shutil.copyfileobj(invoice.file, f)

        with open(po_path, "wb") as f:
            shutil.copyfileobj(po.file, f)

        print(f"📄 Files saved: {invoice_filename}, {po_filename}")

        # Extract data from both files using OCR
        print("🔍 Extracting invoice data...")
        invoice_data = extract_data_from_file(invoice_path)

        print("🔍 Extracting PO data...")
        po_data = extract_data_from_file(po_path)

        # Compare invoice and PO
        print("⚖️  Comparing documents...")
        comparison_result = compare_invoice_po(invoice_data, po_data)

        # Store transaction
        transaction = {
            "invoice_vendor": invoice_data.get("vendor", "N/A"),
            "po_vendor": po_data.get("vendor", "N/A"),
            "invoice_total": invoice_data.get("total", 0),
            "po_total": po_data.get("total", 0),
            "invoice_date": invoice_data.get("date", "N/A"),
            "po_date": po_data.get("date", "N/A"),
            "invoice_number": invoice_data.get("invoice_no", "N/A"),
            "po_number": po_data.get("po_no", "N/A"),
            "status": comparison_result["status"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": comparison_result.get("details", {})
        }

        storage.add_transaction(transaction)

        print(f"✅ Processing complete! Status: {comparison_result['status']}")

        return {
            "status": "processed",
            "invoice": invoice_data,
            "po": po_data,
            "result": comparison_result,
            "transaction_id": len(storage.transactions)
        }

    except Exception as e:
        print(f"❌ Error processing files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.get("/export")
async def export_transactions():
    """
    Export all verified transactions to CSV

    Returns:
        CSV file download
    """
    try:
        if not storage.transactions:
            raise HTTPException(
                status_code=404,
                detail="No transactions found. Please upload and process files first."
            )

        # Generate CSV
        csv_path = export_to_csv(storage.transactions, output_dir=settings.EXPORT_DIR)

        return FileResponse(
            path=csv_path,
            filename=f"futurix_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            media_type="text/csv"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


@app.get("/history")
async def get_history(limit: Optional[int] = 10):
    """
    Get last N processed transactions

    Args:
        limit: Number of transactions to return (default: 10)

    Returns:
        List of recent transactions
    """
    try:
        transactions = storage.transactions[-limit:] if limit > 0 else storage.transactions
        transactions.reverse()  # Show most recent first

        return {
            "total_transactions": len(storage.transactions),
            "showing": len(transactions),
            "transactions": transactions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History error: {str(e)}")


@app.delete("/reset")
async def reset_storage():
    """
    Clear all stored transactions (for testing)

    Returns:
        Confirmation message
    """
    storage.clear()
    return {
        "message": "All transactions cleared",
        "total_transactions": 0
    }


@app.get("/stats")
async def get_statistics():
    """
    Get processing statistics

    Returns:
        Statistics about processed transactions
    """
    total = len(storage.transactions)
    matched = sum(1 for t in storage.transactions if "MATCHED" in t["status"])
    mismatched = total - matched

    return {
        "total_processed": total,
        "matched": matched,
        "mismatched": mismatched,
        "match_rate": f"{(matched/total*100):.2f}%" if total > 0 else "0%"
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Futurix AI Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

