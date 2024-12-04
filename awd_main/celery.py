import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awd_main.settings')

#set up new celery application
app = Celery('awd_main')

#app.config_from_object(f'django.conf:{settings.__name__}', namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')

#load task modules from all registered Django apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')