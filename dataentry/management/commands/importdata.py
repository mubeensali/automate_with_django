from django.core.management.base import BaseCommand, CommandError
#from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError

class Command(BaseCommand):
    help ='Import data from csv file'

    def add_arguments(self, parser) -> None:
        parser.add_argument('file_path', type=str, help='Path to the csv file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        file_path =kwargs['file_path']
        model_name=kwargs['model_name'].capitalize()
        #print(file_path)

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
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            #compare csv header with model field name
            if csv_header !=model_fields:
                raise DataError(f'CSV file doen t match with the {model_name} table fields')

            for row in reader:
                #print(row)
                #Student.objects.create(**row)
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from csv successfully'))