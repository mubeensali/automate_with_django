from django.core.management.base import BaseCommand, CommandError
#from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError
from dataentry.utils import check_csv_errors

class Command(BaseCommand):
    help ='Import data from csv file'

    def add_arguments(self, parser) -> None:
        parser.add_argument('file_path', type=str, help='Path to the csv file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        file_path =kwargs['file_path']
        model_name=kwargs['model_name'].capitalize()
        #print(file_path)

        model = check_csv_errors(file_path, model_name)
        
        with open(file_path,'r')as file:
            reader =csv.DictReader(file)
            for row in reader:
                #print(row)
                #Student.objects.create(**row)
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from csv successfully'))