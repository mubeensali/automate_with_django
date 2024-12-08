from django.shortcuts import render,redirect
from .task import send_email_task
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber


def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST,request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            #send email

            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            #to_email = settings.DEFAULT_TO_EMAIL # to send it default email
            email_list = request.POST.get('email_list')
            print(email_list,'----get the email list id----')

            #Access the selected email list
            email_list = email_form.email_list
            print(email_list,'----email list name----')

            #Extract emal address from the subscribe model
            suscribers =Subscriber.objects.filter(email_list=email_list)

            # convert this snippet to list comprehensive
            #to_email =[]
            #for email in suscribers:
            #    to_email.append(email.email_address)

            to_email =[email.email_address for email in suscribers]

            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment =None            

            #Handover email sending task to celery
            send_email_task.delay(mail_subject,message,to_email,attachment)

            
            #send_email_notification(mail_subject,message,to_email,attachment) # use this function if not using celery

            #Display a Success message
            messages.success(request,'Email sent successfully')
            return redirect('send_email')
    else:
        email_form= EmailForm()
        context ={
            'email_form': email_form,
        }
    return render(request,'emails/send-email.html',context)
