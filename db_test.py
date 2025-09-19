#!/usr/bin/env python
import os
import sys

print("=== DATABASE CONNECTION TEST ===")

# Test the database URL
DATABASE_URL = "postgresql://capitalxdb_user:cErzFTrAr2uuJ180NybFaWBVnr2gMLdI@dpg-d30rrh7diees7389fulg-a/capitalxdb"
print(f"Testing DATABASE_URL: {DATABASE_URL}")

try:
    import dj_database_url
    parsed = dj_database_url.parse(DATABASE_URL)
    print("Database URL parsed successfully:")
    for key, value in parsed.items():
        if key == 'PASSWORD':
            print(f"  {key}: {'*' * len(str(value)) if value else 'None'}")
        else:
            print(f"  {key}: {value}")
except Exception as e:
    print(f"Error parsing database URL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test direct connection
try:
    import psycopg2
    print("Attempting direct database connection...")
    conn = psycopg2.connect(
        dbname=parsed.get('NAME', ''),
        user=parsed.get('USER', ''),
        password=parsed.get('PASSWORD', ''),
        host=parsed.get('HOST', ''),
        port=parsed.get('PORT', '')
    )
    print("Direct connection successful!")
    
    # List existing tables
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()
    print("Existing tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.close()
    conn.close()
    print("Database test completed successfully!")
except Exception as e:
    print(f"Error with direct database connection: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=== DATABASE CONNECTION TEST PASSED ===")