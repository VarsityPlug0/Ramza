from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
import os
import sys

class Command(BaseCommand):
    help = 'Run migrations automatically'

    def handle(self, *args, **options):
        self.stdout.write('Running migrations...')
        
        try:
            # Run migrations
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            self.stdout.write('Migrations completed successfully!')
        except Exception as e:
            self.stdout.write(f'Error running migrations: {e}')
            raise