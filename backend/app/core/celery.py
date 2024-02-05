import os
# Celery Imports
from celery import Celery
# .env Imports
from dotenv import load_dotenv

load_dotenv()
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

celery = Celery("tasks", broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)
