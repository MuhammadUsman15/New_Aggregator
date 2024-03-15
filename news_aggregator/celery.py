import os

from celery import Celery
from celery.schedules import crontab

# Set the default broker URL (adjust as needed)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')

# Set the Django settings module
CELERY_CONFIG_MODULE = 'news_aggregator.settings'

app = Celery('news_aggregator')

# Configure Celery Beat (optional, see next step)
CELERY_BEAT_SCHEDULE = {
    "update_feed_cache": {
        "task": "news.tasks.update_feed_cache",
        "schedule": crontab(minute='*/60'),  # Every 60 minutes (adjust as needed)
    },
}

app.config_from_object(__name__)  # Call this after creating the app instance

app.autodiscover_tasks()  # Automatically discover tasks defined in your project
