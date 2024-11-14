from celery import Celery
from core.config import config

celery_app = Celery(
    "celery_app", 
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL
)

# Ensure Celery is aware of the tasks module
celery_app.conf.update(
    result_expires=3600,
    task_serializer="json",
    accept_content=["json"],
)