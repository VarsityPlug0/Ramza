#!/usr/bin/env python
import psycopg2

print("=== SIMPLE DATABASE TEST ===")
print("Attempting to connect to database...")

try:
    conn = psycopg2.connect(
        database='capitalxdb',
        user='capitalxdb_user',
        password='cErzFTrAr2uuJ180NybFaWBVnr2gMLdI',
        host='dpg-d30rrh7diees7389fulg-a',
        port='5432'
    )
    print("Connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    result = cursor.fetchone()
    if result:
        version = result[0]
        print(f"Database version: {version}")
    else:
        print("No version information returned")
    
    cursor.close()
    conn.close()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Connection failed: {e}")
    import traceback
    traceback.print_exc()