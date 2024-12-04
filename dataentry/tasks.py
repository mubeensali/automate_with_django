from awd_main.celery import app
import time
from django.core.management import call_command
from django.conf import settings
from .utils import send_email_notification

@app.task
def celery_test_task():
    #Execute time consuming task
    time.sleep(10) 
    #Test Email
    mail_subject = 'Test Subject'
    message ='Test msg'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.DEFAULT_TO_EMAIL

    send_email_notification(mail_subject,mail_subject,to_email)    

    return 'email sent sussfully'

@app.task
def import_data_task(file_path,model_name):
    try:
        call_command('importdata',file_path,model_name)                 
    except Exception as e:
    #raise e
        raise e
    # notify the user by email
    email_subject = 'Import Data completed'
    message = 'Your data import has been successful'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(email_subject,message,to_email)
    return 'Data imported successfully'
    