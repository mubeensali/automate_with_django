import datetime
import hashlib
import time
from django.apps import apps
from django.core.management.base import CommandError
import csv
import os
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
from emails.models import Email,Sent,EmailTracking,Subscriber

def get_all_custom_models():
    default_models=['ContentType','Session','LogEntry','Group','Permission','User','Upload']
    custom_models =[]
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
        #print(model)
    return custom_models

def check_csv_errors(file_path, model_name):
#search for the model across all installed apps
    model = None
    for app_config in apps.get_app_configs():
        #Try to search for the model inside the app
        try:
            model=apps.get_model(app_config.label,model_name)
            break # searching stoped once the model is found
        except LookupError:
            continue # model not found in this app, continue searching in next app
    if not model:
        raise CommandError(f'Model "{model_name}" not found in any app!')
    
        #get all the field names of the model
    model_fields = [field.name for field in model._meta.fields if field.name !='id']
    print(model_fields)

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            #compare csv header with model field name
            if csv_header !=model_fields:
                raise DataError(f'CSV file doen t match with the {model_name} table fields')
    except Exception as e:
        raise e
    
    return model

def send_email_notification(mail_subject,message,to_email,attachment=None,email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        #mail = EmailMessage(mail_subject,message,from_email, to=[to_email])# if the email is not in list use this func

        for recipient_email in to_email:
            # Create Emailtraching record
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list,email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email=email,
                    subscriber = subscriber,
                    unique_id = unique_id,
                )
            # 
            # Generate the tracking pixel
            # 
            # search for the links in the email body
            # 
            # If there are links  or urls in the email body, inject our click tracking url to that orginal link           
            mail = EmailMessage(mail_subject,message,from_email, to=to_email)
            if attachment is not None:
                mail.attach_file(attachment)

            mail.content_subtype = 'html'
            mail.send()
        # Store the send email inside the sent model
        if email:
            sent = Sent()
            sent.email =email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e
    
def generate_csv_file(model_name):
    # generate the timestampe of current data and time
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    #define the csv file name/ file/path
    exported_dir = 'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path =os.path.join(settings.MEDIA_ROOT, exported_dir,file_name)
    print(file_path,'-----file path ------')
    return file_path
