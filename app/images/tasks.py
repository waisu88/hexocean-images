from app.celery import app as celeryapp
from .models import ExpiringLink
import time
from celery import shared_task

@shared_task()
def delete_expiring_link(params):
    object = ExpiringLink.objects.get(id=params["instance_id"])
    time.sleep(params["seconds"])
    object.delete()





