#!/usr/bin/env python
import os
import sys

# Test database URL directly
DATABASE_URL = "postgresql://capitalxdb_user:cErzFTrAr2uuJ180NybFaWBVnr2gMLdI@dpg-d30rrh7diees7389fulg-a/capitalxdb"

print("=== Testing Database URL ===")
print(f"DATABASE_URL: {DATABASE_URL}")

# Try to parse it
try:
    import dj_database_url
    parsed = dj_database_url.parse(DATABASE_URL)
    print("Parsed database configuration:")
    for key, value in parsed.items():
        if key == 'PASSWORD':
            print(f"  {key}: {'*' * len(str(value)) if value else 'None'}")
        else:
            print(f"  {key}: {value}")
    print("Database URL parsing successful!")
except Exception as e:
    print(f"Error parsing database URL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Try to connect directly with psycopg2
try:
    import psycopg2
    print("Attempting direct connection...")
    conn = psycopg2.connect(
        dbname=parsed.get('NAME', ''),
        user=parsed.get('USER', ''),
        password=parsed.get('PASSWORD', ''),
        host=parsed.get('HOST', ''),
        port=parsed.get('PORT', '')
    )
    print("Direct connection successful!")
    conn.close()
except Exception as e:
    print(f"Error connecting directly: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("All tests passed!")