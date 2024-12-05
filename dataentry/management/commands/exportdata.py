import csv
from django.core.management.base import BaseCommand, CommandParser
from django.apps import apps
import datetime
from dataentry.utils import generate_csv_file
# proposed command python manage.py exportdata modelname

class Command(BaseCommand):
    help ='Export data from Database model to a CSV file'
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Model name')

    def handle(self, *args, **kwargs) -> str | None:
        model_name=kwargs['model_name'].capitalize()

        #search through all the installed apps for the model
        model=None
        for app_config in apps.get_app_configs():
            #try searching for the model
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass
        if not model:
            self.stderr.write(f'Model {model_name} could not found')
            return
                    
        # fetch the data from the database
        data = model.objects.all()

        # generate csv file path
        file_path = generate_csv_file(model_name)


        #open the csv file and write data
        with open(file_path,'w',newline='') as file:
            writer = csv.writer(file)
            # first it will write header
            #print the fields name of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields])

            #write data rows
            for dt in data:
                writer.writerow([getattr(dt,field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))