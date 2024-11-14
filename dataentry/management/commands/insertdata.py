from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help ='It will insert data to the database using command'

    def handle(self, *args, **kwargs):
        dataset=[
            {'roll_no':102,'name':'Django', 'age':30},
            {'roll_no':103,'name':'John', 'age':36},
            {'roll_no':104,'name':'Mike', 'age':32},
            ]
        for data in dataset:
            #print(data['name'])
            Student.objects.create(roll_no=data['roll_no'],name=data['name'],age=data['age'])
        #Student.objects.create(roll_no=101,name='Mubeen',age=20)
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))