import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_service.settings')


app = Celery('post_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    timezone = settings.TIME_ZONE
)
app.autodiscover_tasks()
