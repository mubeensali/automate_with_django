from typing import Any
from django.core.management.base import BaseCommand, CommandParser

# Propsed command is python manage.py greeting name
#o/p will be Assalamualikum  {Name}
class Command(BaseCommand):
    help = 'Greets the user'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('name', type=str, help='Specifies user name')
        #return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        name =options['name']
        greeting = f'Assalamu alikum, {name}'
        #self.stdout.write(greeting)
        #self.stderr.write(greeting)
        self.stdout.write(self.style.SUCCESS(greeting))
        #self.stdout.write(self.style.WARNING(greeting))
        #return super().handle(*args, **options)