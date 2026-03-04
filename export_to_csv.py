#!/usr/bin/env python3
"""
SQLite3 Database to CSV Export Script
Export all tables to individual CSV files
"""

import sqlite3
import csv
from datetime import datetime

# Register datetime converters
sqlite3.register_adapter(datetime, lambda val: val.isoformat())
sqlite3.register_converter("timestamp", lambda val: datetime.fromisoformat(val.decode()) if isinstance(val, bytes) else val)

def export_table_to_csv(cursor, table_name):
    """Export a table to CSV file"""
    try:
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Get all data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Create CSV filename
        csv_filename = f"{table_name}.csv"
        
        # Write to CSV
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(columns)
            
            # Write data rows
            writer.writerows(rows)
        
        print(f"✅ {csv_filename:<30} - {len(rows):>4} records exported")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting '{table_name}': {e}")
        return False

def export_all_tables():
    """Export all tables to CSV files"""
    try:
        # Connect to database
        conn = sqlite3.connect('patient_db.sqlite3', detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        
        print("\n" + "="*70)
        print("🏥 EXPORTING DATABASE TABLES TO CSV")
        print("="*70 + "\n")
        
        # Get list of all tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("❌ No tables found in database")
            conn.close()
            return
        
        print(f"📊 Found {len(tables)} tables\n")
        
        # Export each table
        success_count = 0
        for table in tables:
            if export_table_to_csv(cursor, table):
                success_count += 1
        
        conn.close()
        
        print("\n" + "="*70)
        print(f"✅ EXPORT COMPLETE - {success_count}/{len(tables)} tables exported")
        print("="*70 + "\n")
        
        # Show file list
        print("📁 CSV files created:")
        for table in tables:
            print(f"   - {table}.csv")
        print()
        
    except sqlite3.OperationalError as e:
        print(f"\n❌ Database Error: {e}")
        print("💡 Make sure you've run SQLITE3_DATA.py first to create the database!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    export_all_tables()
