#!/usr/bin/env python3
"""
Healthcare Database - Delete All Data
Removes all data from all tables while keeping table structure intact
"""

import sqlite3
from datetime import datetime


def delete_all_data(db_path: str = 'patient_db.sqlite3', confirm: bool = True):
    """
    Delete all data from all tables in the database
    
    Args:
        db_path: Path to SQLite database file
        confirm: If True, asks for confirmation before deleting
    """
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*70)
        print("🗑️  DATABASE DATA DELETION TOOL")
        print("="*70 + "\n")
        
        print(f"📁 Database: {db_path}\n")
        
        # List of tables to clear
        tables = [
            'vitals',
            'audit_logs',
            'triage_rules',
            'patients',
            'doctors',
            'resources',
            'users',
            'wards'
        ]
        
        # Show current record counts
        print("📊 Current Record Counts:")
        print("-" * 70)
        total_records = 0
        for table in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                total_records += count
                print(f"   {table:<25} : {count:>6} records")
            except sqlite3.OperationalError:
                print(f"   {table:<25} : Table not found")
        
        print("-" * 70)
        print(f"   {'TOTAL':<25} : {total_records:>6} records\n")
        
        if total_records == 0:
            print("ℹ️  Database is already empty. Nothing to delete.\n")
            conn.close()
            return
        
        # Confirmation
        if confirm:
            response = input("⚠️  Are you sure you want to DELETE ALL DATA? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("❌ Deletion cancelled.\n")
                conn.close()
                return
        
        # Delete data from all tables
        print("\n🔄 Deleting data...")
        print("-" * 70)
        
        deleted_count = 0
        for table in tables:
            try:
                cursor.execute(f'DELETE FROM {table}')
                rows_deleted = cursor.rowcount
                deleted_count += rows_deleted
                status = "✅" if rows_deleted > 0 else "⏭️ "
                print(f"   {status} {table:<25} : {rows_deleted:>6} records deleted")
            except sqlite3.OperationalError as e:
                print(f"   ⚠️  {table:<25} : Error - {e}")
        
        conn.commit()
        print("-" * 70)
        
        # Verify deletion
        print("\n✔️  Verifying deletion...")
        print("-" * 70)
        
        verify_count = 0
        for table in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                verify_count += count
                status = "✅" if count == 0 else "❌"
                print(f"   {status} {table:<25} : {count:>6} records")
            except sqlite3.OperationalError:
                pass
        
        print("-" * 70)
        
        conn.close()
        
        if verify_count == 0:
            print(f"\n✅ SUCCESS! Deleted {deleted_count} records from all tables")
            print("📋 Table structure preserved (ready for new data)\n")
        else:
            print(f"\n⚠️  {verify_count} records still remain in database\n")
    
    except sqlite3.Error as e:
        print(f"\n❌ Database Error: {e}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


def delete_specific_table(db_path: str = 'patient_db.sqlite3', table_name: str = None):
    """
    Delete data from a specific table only
    
    Args:
        db_path: Path to SQLite database file
        table_name: Name of the table to clear
    """
    
    if not table_name:
        print("❌ Error: Table name is required\n")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*70)
        print(f"🗑️  DELETE DATA FROM TABLE: {table_name}")
        print("="*70 + "\n")
        
        # Check if table exists and get record count
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        
        print(f"📁 Database: {db_path}")
        print(f"📋 Table: {table_name}")
        print(f"📊 Records to delete: {count}\n")
        
        if count == 0:
            print("ℹ️  Table is already empty.\n")
            conn.close()
            return
        
        # Confirmation
        response = input(f"⚠️  Delete all {count} records from '{table_name}'? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("❌ Deletion cancelled.\n")
            conn.close()
            return
        
        # Delete data
        cursor.execute(f'DELETE FROM {table_name}')
        conn.commit()
        
        # Verify
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        remaining = cursor.fetchone()[0]
        
        conn.close()
        
        if remaining == 0:
            print(f"\n✅ SUCCESS! Deleted {count} records from '{table_name}'\n")
        else:
            print(f"\n⚠️  {remaining} records still remain\n")
    
    except sqlite3.OperationalError as e:
        print(f"\n❌ Table Error: {e}\n")
    except sqlite3.Error as e:
        print(f"\n❌ Database Error: {e}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Delete all data from SQLite healthcare database"
    )
    parser.add_argument(
        '--db',
        default='patient_db.sqlite3',
        help='Path to SQLite database (default: patient_db.sqlite3)'
    )
    parser.add_argument(
        '--table',
        help='Delete data from specific table only (optional)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    args = parser.parse_args()
    
    if args.table:
        delete_specific_table(args.db, args.table)
    else:
        delete_all_data(args.db, confirm=not args.force)


if __name__ == '__main__':
    main()