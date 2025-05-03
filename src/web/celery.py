import os

from celery import Celery
from celery.schedules import crontab

from web import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery(
    'web',
    backend=settings.CELERY_RESULT_BACKEND,
    broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notification_users': {
        'task': 'app_notification.tasks.notification_users_task',
        'schedule': crontab(minute='0,10,20,30,40,50'),
    }
}
