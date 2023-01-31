from celery.schedules import crontab
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('celery_worker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery beat tasks

app.conf.beat_schedule = {
    'send-spam-every-1-minute': {
        'task': 'users.tasks.celery_beat_task',
        'schedule': crontab(minute='*/1'),
    }
}