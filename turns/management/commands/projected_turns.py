from django.core.management.base import BaseCommand, CommandError

# import additional classes/modules as needed
from turns.models import Turn
from datetime import date


class Command(BaseCommand):
    help = 'Projected turns for a given date in format YY-MM-DD'

    def add_arguments(self, parser):
        parser.add_argument('--date', nargs='+', type=date.fromisoformat, help="Date in YY-MM-DD format")

    def handle(self, *args, **options):
        try:
            requested_date: date = options.get('date')[0]
            result = Turn.projected_turns(requested_date)
            print(f'Projected turns for date {requested_date}: {result}')
        except Exception as e:
            raise CommandError(e.args[0])
