"""Celery application configuration."""

from celery import Celery
from celery.schedules import crontab
from app.core.config import get_settings

settings = get_settings()

# Create Celery instance
celery_app = Celery(
    "futurix_ai",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.services.email_service",
        "app.services.shivaay_ai",
        "app.services.verification_service",
        "app.services.csv_service",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Celery Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "periodic-email-scan": {
        "task": "app.services.email_service.periodic_email_scan",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
    "generate-csv-snapshot": {
        "task": "app.services.csv_service.generate_csv_snapshot",
        "schedule": crontab(hour="*/6"),  # Every 6 hours
    },
}

