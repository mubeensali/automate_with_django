from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task

def home(request):
    return render(request,'home.html')

def celery_test(request):
    #Execute time consuming task
    #time.sleep(10) #this task takes 10 seconds. this is taking 10 sec to run. so will give it to celery task
    celery_test_task.delay()
    return HttpResponse('<h3>Function executed successfullly</h3>')