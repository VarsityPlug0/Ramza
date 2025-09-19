from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
import os
import sys

class Command(BaseCommand):
    help = 'Run migrations automatically'

    def handle(self, *args, **options):
        self.stdout.write('Running migrations...')
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate'])
        
        self.stdout.write('Migrations completed successfully!')