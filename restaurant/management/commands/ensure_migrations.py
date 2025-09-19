from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
import sys

class Command(BaseCommand):
    help = 'Ensure all migrations are applied'

    def handle(self, *args, **options):
        self.stdout.write('Ensuring all migrations are applied...')
        
        try:
            # Run migrations for all apps
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            
            # Verify that the auth tables exist
            with connection.cursor() as cursor:
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'auth_user')")
                auth_user_exists = cursor.fetchone()[0]
                
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'restaurant_sitesettings')")
                sitesettings_exists = cursor.fetchone()[0]
                
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'restaurant_contentsection')")
                contentsection_exists = cursor.fetchone()[0]
                
            if auth_user_exists and sitesettings_exists and contentsection_exists:
                self.stdout.write('All required tables exist. Migrations applied successfully!')
            else:
                self.stdout.write('Warning: Some tables may be missing.')
                
        except Exception as e:
            self.stdout.write(f'Error ensuring migrations: {e}')
            raise