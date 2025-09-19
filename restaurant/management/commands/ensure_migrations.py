from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
import sys

class Command(BaseCommand):
    help = 'Ensure all migrations are applied'

    def handle(self, *args, **options):
        self.stdout.write('Ensuring all migrations are applied...')
        
        try:
            # Show which migrations are available
            self.stdout.write('Checking available migrations...')
            execute_from_command_line(['manage.py', 'showmigrations'])
            
            # Run migrations for all apps
            self.stdout.write('Running migrations...')
            execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
            
            # Verify that the auth tables exist
            self.stdout.write('Verifying required tables exist...')
            with connection.cursor() as cursor:
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'auth_user')")
                auth_user_exists = cursor.fetchone()[0]
                
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'restaurant_sitesettings')")
                sitesettings_exists = cursor.fetchone()[0]
                
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'restaurant_contentsection')")
                contentsection_exists = cursor.fetchone()[0]
                
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'restaurant_siteimage')")
                siteimage_exists = cursor.fetchone()[0]
                
            self.stdout.write(f"auth_user table exists: {auth_user_exists}")
            self.stdout.write(f"restaurant_sitesettings table exists: {sitesettings_exists}")
            self.stdout.write(f"restaurant_contentsection table exists: {contentsection_exists}")
            self.stdout.write(f"restaurant_siteimage table exists: {siteimage_exists}")
                
            if auth_user_exists and sitesettings_exists and contentsection_exists and siteimage_exists:
                self.stdout.write('SUCCESS: All required tables exist. Migrations applied successfully!')
            else:
                missing = []
                if not auth_user_exists:
                    missing.append('auth_user')
                if not sitesettings_exists:
                    missing.append('restaurant_sitesettings')
                if not contentsection_exists:
                    missing.append('restaurant_contentsection')
                if not siteimage_exists:
                    missing.append('restaurant_siteimage')
                    
                self.stdout.write(f'WARNING: Missing tables: {", ".join(missing)}')
                
        except Exception as e:
            self.stdout.write(f'ERROR: Failed to ensure migrations: {e}')
            raise