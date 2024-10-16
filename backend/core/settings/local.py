from .base import *  # noqa
from dotenv import load_dotenv
import dj_database_url
import os

# Load environment variables from .env file
load_dotenv()

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv(
            "DATABASE_URL", "postgres://project:password@db:5432/project"
        ),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
