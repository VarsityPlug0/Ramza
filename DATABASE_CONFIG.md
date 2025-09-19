# Database Configuration

## Current Setup

The application is configured to use the specified PostgreSQL database for deployment on Render:

**Connection String**: `postgresql://capitalxdb_user:cErzFTrAr2uuJ180NybFaWBVnr2gMLdI@dpg-d30rrh7diees7389fulg-a/capitalxdb`

## Implementation Details

1. **Primary Database**: PostgreSQL database hosted externally
2. **Fallback Mechanism**: SQLite for local development when PostgreSQL is not accessible
3. **Deployment**: Uses the external PostgreSQL database via render.yaml configuration

## Configuration Files

### settings.py
```python
if 'DATABASE_URL' in os.environ:
    # Render deployment database
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
else:
    # Local development database - try PostgreSQL first, fallback to SQLite
    try:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'capitalxdb',
                'USER': 'capitalxdb_user',
                'PASSWORD': 'cErzFTrAr2uuJ180NybFaWBVnr2gMLdI',
                'HOST': 'dpg-d30rrh7diees7389fulg-a',
                'PORT': '5432',
            }
        }
        # Test the connection
        import psycopg2
        conn = psycopg2.connect(
            dbname='capitalxdb',
            user='capitalxdb_user',
            password='cErzFTrAr2uuJ180NybFaWBVnr2gMLdI',
            host='dpg-d30rrh7diees7389fulg-a',
            port='5432'
        )
        conn.close()
    except:
        # Fallback to SQLite if PostgreSQL is not accessible
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
```

### render.yaml
```yaml
services:
  - type: web
    name: ramzas-chillas
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn fastfood_restaurant.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: DATABASE_URL
        value: "postgresql://capitalxdb_user:cErzFTrAr2uuJ180NybFaWBVnr2gMLdI@dpg-d30rrh7diees7389fulg-a/capitalxdb"
      - key: SECRET_KEY
        sync: false
      - key: WEB_CONCURRENCY
        value: 4
```

## Verification

The database configuration has been verified with:
- `python manage.py check` - Passed with no issues
- `python manage.py showmigrations` - Successfully listed all migrations
- `python manage.py check --deploy` - Passed with only standard security warnings

The application will use PostgreSQL when deployed on Render and fall back to SQLite for local development.