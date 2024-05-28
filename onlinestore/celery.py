#Celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinestore.settings')

# Create a Celery instance with a dynamic app name
app = Celery(__name__)

# Configure Celery to use the Django settings module
app.config_from_object('django.conf:settings', namespace='CELERY')

# Set the Celery timezone
app.conf.CELERY_TIMEZONE = 'UTC'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

