#!/usr/bin/env python3
"""
Healthcare Database Data Loader
Simple script to create tables and load sample data using SQLAlchemy
No external imports required - works directly with your database
"""

import sqlite3
from datetime import datetime

conn = sqlite3.connect('triage.db')
cursor = conn.cursor()


def load_wards(cursor, conn):
    """Load ward data"""
    print("\n📍 Loading Wards...")
    wards_data = [
        ("Emergency",),
        ("ICU",),
        ("Cardiology",),
        ("Neurology",),
        ("Pediatrics",),
        ("General Ward",),
        ("Trauma Center",),
        ("Recovery",),
    ]
    
    cursor.executemany('INSERT INTO wards (name) VALUES (?)', wards_data)
    conn.commit()
    print(f"✅ {len(wards_data)} wards loaded")


def load_doctors(cursor, conn):
    """Load doctor data"""
    print("\n👨‍⚕️  Loading Doctors...")
    doctors_data = [
        ("Dr. Rajesh Kumar", "Emergency", 5),
        ("Dr. Priya Singh", "ICU", 3),
        ("Dr. Amit Patel", "Cardiology", 4),
        ("Dr. Neha Sharma", "Neurology", 2),
        ("Dr. Vikas Gupta", "Pediatrics", 6),
        ("Dr. Anjali Verma", "General Ward", 8),
        ("Dr. Rohan Singh", "Trauma Center", 7),
        ("Dr. Sneha Kapoor", "Recovery", 4),
    ]
    
    cursor.executemany(
        'INSERT INTO doctors (name, ward, active_patients) VALUES (?, ?, ?)',
        doctors_data
    )
    conn.commit()
    print(f"✅ {len(doctors_data)} doctors loaded")


def load_users(cursor, conn):
    """Load user data"""
    print("\n👥 Loading Users...")
    users_data = [
        # ("admin@hospital.com", "hashed_pwd_123", "admin"),
        ("doctor1@hospital.com", "hashed_pwd_124", "doctor"),
        ("doctor2@hospital.com", "hashed_pwd_125", "doctor"),
        ("nurse1@hospital.com", "hashed_pwd_126", "nurse"),
        ("nurse2@hospital.com", "hashed_pwd_127", "nurse"),
        ("receptionist@hospital.com", "hashed_pwd_128", "receptionist"),
        ("technician@hospital.com", "hashed_pwd_129", "technician"),
        ("supervisor@hospital.com", "hashed_pwd_130", "supervisor"),
    ]
    
    cursor.executemany(
        'INSERT INTO users (email, password, role) VALUES (?, ?, ?)',
        users_data
    )
    conn.commit()
    print(f"✅ {len(users_data)} users loaded")


def load_resources(cursor, conn):
    """Load hospital resource data"""
    print("\n🏥 Loading Resources...")
    resources_data = [
        ("Oxygen Cylinders", 150, 45),
        ("ICU Beds", 20, 18),
        ("Ventilators", 15, 12),
        ("ECG Machines", 10, 7),
        ("Blood Pressure Monitors", 50, 35),
        ("Pulse Oximeters", 40, 28),
        ("Thermometers", 100, 85),
        ("Stretchers", 30, 22),
        ("Wheelchairs", 25, 15),
        ("Emergency Kits", 20, 8),
    ]
    
    cursor.executemany(
        'INSERT INTO resources (name, total, used) VALUES (?, ?, ?)',
        resources_data
    )
    conn.commit()
    print(f"✅ {len(resources_data)} resources loaded")


def load_patients(cursor, conn):
    """Load patient data"""
    print("\n🏥 Loading Patients...")
    patients_data = [
        ("Ramesh Kumar", 45, "Male", "Dr. Rajesh Kumar", "Emergency", 78, 98, 98.6, 120, "Moderate", "Admitted"),
        ("Deepika Sharma", 32, "Female", "Dr. Priya Singh", "ICU", 92, 94, 99.2, 138, "Critical", "Admitted"),
        ("Arjun Singh", 58, "Male", "Dr. Amit Patel", "Cardiology", 85, 96, 98.4, 145, "High", "Admitted"),
        ("Priya Verma", 28, "Female", "Dr. Neha Sharma", "Neurology", 72, 99, 98.2, 115, "Low", "Admitted"),
        ("Rohan Gupta", 7, "Male", "Dr. Vikas Gupta", "Pediatrics", 95, 97, 99.5, 95, "Low", "Admitted"),
        ("Anjali Singh", 42, "Female", "Dr. Anjali Verma", "General Ward", 76, 98, 98.8, 125, "Low", "Admitted"),
        ("Vikram Patel", 35, "Male", "Dr. Rohan Singh", "Trauma Center", 110, 92, 99.8, 155, "Critical", "Admitted"),
        ("Sneha Kapoor", 50, "Female", "Dr. Sneha Kapoor", "Recovery", 72, 99, 98.0, 120, "Low", "Recovery"),
    ]
    
    cursor.executemany(
        '''INSERT INTO patients 
           (name, age, gender, doctor, ward, heart_rate, oxygen_level, temperature, blood_pressure, severity, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        patients_data
    )
    conn.commit()
    print(f"✅ {len(patients_data)} patients loaded")


def load_vitals(cursor, conn):
    """Load patient vitals history"""
    print("\n📊 Loading Vitals...")
    
    # Get all patients
    cursor.execute('SELECT id, heart_rate, oxygen_level, blood_pressure, temperature FROM patients')
    patients = cursor.fetchall()
    
    vitals_data = []
    for patient in patients:
        patient_id, hr, o2, bp, temp = patient
        # Create 3 readings per patient
        for i in range(3):
            vitals_data.append((
                patient_id,
                hr + (i * 5),
                o2 - (i * 0.5),
                bp + (i * 3),
                temp + (i * 0.1)
            ))
    
    cursor.executemany(
        '''INSERT INTO vitals (patient_id, heart_rate, oxygen_level, blood_pressure, temperature)
           VALUES (?, ?, ?, ?, ?)''',
        vitals_data
    )
    conn.commit()
    print(f"✅ {len(vitals_data)} vital records loaded")


def load_triage_rules(cursor, conn):
    """Load triage rules"""
    print("\n⚙️  Loading Triage Rules...")
    rules_data = [
        ("heart_rate", ">", 100.0, "Critical", "ICU"),
        ("heart_rate", ">", 85.0, "High", "Cardiology"),
        ("oxygen_level", "<", 94.0, "Critical", "ICU"),
        ("oxygen_level", "<", 96.0, "High", "Emergency"),
        ("temperature", ">", 39.0, "Critical", "Isolation"),
        ("temperature", ">", 38.5, "High", "General Ward"),
        ("blood_pressure", ">", 160.0, "Critical", "Cardiology"),
        ("blood_pressure", ">", 140.0, "High", "Emergency"),
        ("heart_rate", "<", 50.0, "Critical", "ICU"),
        ("blood_pressure", "<", 90.0, "Critical", "ICU"),
    ]
    
    cursor.executemany(
        '''INSERT INTO triage_rules (parameter, operator, threshold, category, ward)
           VALUES (?, ?, ?, ?, ?)''',
        rules_data
    )
    conn.commit()
    print(f"✅ {len(rules_data)} triage rules loaded")


def load_audit_logs(cursor, conn):
    """Load audit log entries"""
    print("\n📋 Loading Audit Logs...")
    audit_data = [
        ("System initialized", 1),
        ("Patient admitted", 1),
        ("Vitals recorded", 1),
        ("Patient transferred", 2),
        ("Doctor assigned", 1),
        ("Resource allocated", 3),
        ("Patient discharged", 1),
        ("Triage rule applied", 4),
        ("Report generated", 2),
        ("System backup", 5),
    ]
    
    cursor.executemany(
        'INSERT INTO audit_logs (action, user_id) VALUES (?, ?)',
        audit_data
    )
    conn.commit()
    print(f"✅ {len(audit_data)} audit logs loaded")


def print_summary(cursor):
    """Print database summary"""
    print("\n" + "="*70)
    print("📊 DATABASE SUMMARY")
    print("="*70 + "\n")
    
    tables = {
        'wards': 'Wards',
        'doctors': 'Doctors',
        'users': 'Users',
        'patients': 'Patients',
        'resources': 'Resources',
        'vitals': 'Vital Records',
        'triage_rules': 'Triage Rules',
        'audit_logs': 'Audit Logs'
    }
    
    for table, label in tables.items():
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"   {label:<25} : {count:>4} records")
    
    print("\n✅ Database ready for use!\n")


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🏥 HEALTHCARE DATABASE LOADER")
    print("="*70)
    
    try:
        # Create tables
       
        
        # Load data
      
        
        load_wards(cursor, conn)
        load_doctors(cursor, conn)
        load_users(cursor, conn)
        load_resources(cursor, conn)
        load_patients(cursor, conn)
        load_vitals(cursor, conn)
        load_triage_rules(cursor, conn)
        load_audit_logs(cursor, conn)
        
        # Print summary
        print_summary(cursor)
        
        conn.close()
        print("✅ All operations completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if conn:
            conn.rollback()
            conn.close()


if __name__ == '__main__':
    main()