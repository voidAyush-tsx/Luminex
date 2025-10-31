"""FastAPI application main entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy import text
from app.core.config import get_settings
from app.database import engine, get_db
from app.models import Base
from app.routers import invoices, purchase_orders, verification, email_automation, export
from app.utils.logger import logger

# Initialize settings (may fail if env vars not set - handled in health check)
try:
    settings = get_settings()
except Exception as e:
    logger.warning(f"Settings initialization warning: {e}")
    settings = None

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"Database initialization error: {e}")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name if settings else "Futurix AI Backend",
    version=settings.app_version if settings else "1.0.0",
    description="AI-Powered Invoice & Purchase Order Verification System",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin] if settings else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(invoices.router)
app.include_router(purchase_orders.router)
app.include_router(verification.router)
app.include_router(email_automation.router)
app.include_router(export.router)


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    db_status = "connected"
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Database health check failed: {str(e)}")
    
    try:
        app_settings = get_settings()
    except:
        app_settings = None
    return {
        "app_name": app_settings.app_name if app_settings else "Futurix AI Backend",
        "version": app_settings.app_version if app_settings else "1.0.0",
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

