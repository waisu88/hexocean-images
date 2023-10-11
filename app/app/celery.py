import os
from celery import Celery
from django.conf import settings







os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Warsaw')

app.config_from_object(settings, namespace='CELERY')

# Celery beat settings
app.conf.beat_schedule = {

}


app.autodiscover_tasks()

