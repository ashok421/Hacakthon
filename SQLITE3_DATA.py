#!/usr/bin/env python3
"""
Simple SQLite3 Database Setup & Data Loader
Run once: python setup_database.py
"""

import sqlite3
import random
import os
from datetime import datetime, timedelta

# Register datetime adapters to avoid deprecation warning
sqlite3.register_adapter(datetime, lambda val: val.isoformat())
sqlite3.register_converter("timestamp", lambda val: datetime.fromisoformat(val.decode()))

# ============================================================================
# STEP 1: CREATE DATABASE & TABLES
# ============================================================================

def create_database():
    """Create SQLite database and all tables"""
    print("\n📊 Creating database schema...\n")
    
    # Delete existing database file if it exists
    db_file = 'patient_db.sqlite3'
    if os.path.exists(db_file):
        os.remove(db_file)
        print("🗑️  Deleted existing database file\n")
    
    # Connect to SQLite (creates file if doesn't exist)
    conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    # TABLE 1: Users (Admin & Manager login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Table 'users' created")
    
    # TABLE 2: Patients (Patient records)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT,
            ward TEXT,
            doctor_assigned TEXT,
            heart_rate INTEGER,
            blood_pressure TEXT,
            temperature REAL,
            oxygen_saturation INTEGER,
            diagnosis TEXT,
            admission_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Table 'patients' created")
    
    # TABLE 3: Classification Rules (Rules for categorizing patients)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classification_rules (
            rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT UNIQUE NOT NULL,
            condition_type TEXT,
            min_threshold REAL,
            max_threshold REAL,
            classification_level TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(created_by) REFERENCES users(user_id)
        )
    ''')
    print("✅ Table 'classification_rules' created")
    
    # TABLE 4: Patient Classifications (Results of classification)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_classifications (
            classification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            classification_level TEXT,
            rule_applied_id INTEGER,
            classified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY(rule_applied_id) REFERENCES classification_rules(rule_id)
        )
    ''')
    print("✅ Table 'patient_classifications' created")
    
    conn.commit()
    return conn

# ============================================================================
# STEP 2: LOAD SAMPLE DATA
# ============================================================================

def load_users(conn):
    """Insert Admin and Manager users"""
    print("\n📝 Loading users...\n")
    
    cursor = conn.cursor()
    
    users = [
        ('admin', 'admin123', 'Administrator'),
        ('manager1', 'pass123', 'Manager') 
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)',
        users
    )
    
    conn.commit()
    print(f"✅ Loaded {len(users)} users")
    for user in users:
        print(f"   - {user[0]} ({user[2]})")

def load_rules(conn):
    """Insert classification rules"""
    print("\n📋 Loading classification rules...\n")
    
    cursor = conn.cursor()
    
    # Get admin user ID
    cursor.execute('SELECT user_id FROM users WHERE role = "Administrator" LIMIT 1')
    admin_id = cursor.fetchone()[0]
    
    rules = [
        # CRITICAL RULES
        ('High Heart Rate', 'heart_rate', 120, 200, 'Critical', admin_id),
        ('Low Oxygen', 'oxygen_saturation', 0, 89, 'Critical', admin_id),
        ('High Temperature', 'temperature', 39.0, 42.0, 'Critical', admin_id),
        
        # MODERATE RULES
        ('Elevated Heart Rate', 'heart_rate', 100, 119, 'Moderate', admin_id),
        ('Borderline Oxygen', 'oxygen_saturation', 90, 94, 'Moderate', admin_id),
        ('Elevated Temperature', 'temperature', 37.5, 38.9, 'Moderate', admin_id),
        
        # STABLE RULES
        ('Normal Heart Rate', 'heart_rate', 60, 99, 'Stable', admin_id),
        ('Good Oxygen Level', 'oxygen_saturation', 95, 100, 'Stable', admin_id),
        ('Normal Temperature', 'temperature', 36.0, 37.4, 'Stable', admin_id),
    ]
    
    cursor.executemany(
        '''INSERT OR IGNORE  INTO classification_rules 
           (rule_name, condition_type, min_threshold, max_threshold, classification_level, created_by)
           VALUES (?, ?, ?, ?, ?, ?)''',
        rules
    )
    
    conn.commit()
    print(f"✅ Loaded {len(rules)} classification rules")
    
    # Show rules by category
    for category in ['Critical', 'Moderate', 'Stable']:
        count = len([r for r in rules if r[4] == category])
        print(f"   - {category}: {count} rules")

def load_patients(conn, num_patients=100):
    """Generate and insert patient data"""
    print(f"\n👥 Generating {num_patients} patient records...\n")
    
    cursor = conn.cursor()
    
    # Data lists
    wards = ['ICU', 'Emergency', 'General Ward', 'Cardiology', 'Respiratory']
    doctors = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Davis']
    diagnoses = [
        'Sepsis', 'Pneumonia', 'Heart Attack', 'Stroke', 'Respiratory Failure',
        'Kidney Failure', 'Heart Failure', 'Infection', 'Appendicitis', 'Diabetes'
    ]
    
    patients_to_insert = []
    
    for i in range(1, num_patients + 1):
        # Generate realistic data
        name = f"Patient_{i:03d}"
        age = random.randint(18, 90)
        gender = random.choice(['M', 'F'])
        ward = random.choice(wards)
        doctor = random.choice(doctors)
        
        # Vital signs (realistic ranges)
        heart_rate = random.randint(50, 150)
        sys_bp = random.randint(90, 180)
        dia_bp = random.randint(50, 110)
        blood_pressure = f"{sys_bp}/{dia_bp}"
        temperature = round(random.uniform(36.0, 39.5), 1)
        oxygen_saturation = random.randint(80, 100)
        diagnosis = random.choice(diagnoses)
        
        # Admission date (within last 30 days)
        days_ago = random.randint(0, 30)
        admission_date = datetime.now() - timedelta(days=days_ago)
        
        patients_to_insert.append((
            name, age, gender, ward, doctor, heart_rate,
            blood_pressure, temperature, oxygen_saturation,
            diagnosis, admission_date
        ))
    
    # Insert all at once (faster)
    cursor.executemany(
        '''INSERT or IGNORE  INTO patients 
           (patient_name, age, gender, ward, doctor_assigned, heart_rate,
            blood_pressure, temperature, oxygen_saturation, diagnosis, admission_date)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        patients_to_insert
    )
    
    conn.commit()
    print(f"✅ Generated and loaded {num_patients} patient records")
    print(f"   - Wards: {', '.join(wards)}")
    print(f"   - Doctors: {len(doctors)}")
    print(f"   - Diagnoses: {len(diagnoses)}")

def auto_classify_patients(conn):
    """Automatically classify patients based on rules"""
    print("\n🔄 Auto-classifying patients...\n")
    
    cursor = conn.cursor()
    
    # Get all patients
    cursor.execute('''
        SELECT patient_id, heart_rate, oxygen_saturation, temperature
        FROM patients
    ''')
    patients = cursor.fetchall()
    
    # Get all rules
    cursor.execute('''
        SELECT rule_id, condition_type, min_threshold, max_threshold, classification_level
        FROM classification_rules
    ''')
    rules = cursor.fetchall()
    
    classifications_to_insert = []
    
    # Classify each patient
    for patient_id, heart_rate, o2_sat, temp in patients:
        classification = 'Stable'  # Default
        rule_used = None
        
        # Check each rule (Critical takes priority)
        for rule_id, condition_type, min_val, max_val, class_level in rules:
            match = False
            
            if condition_type == 'heart_rate':
                match = min_val <= heart_rate <= max_val
            elif condition_type == 'oxygen_saturation':
                match = min_val <= o2_sat <= max_val
            elif condition_type == 'temperature':
                match = min_val <= temp <= max_val
            
            if match:
                classification = class_level
                rule_used = rule_id
                # Critical takes priority, stop checking
                if class_level == 'Critical':
                    break
        
        classifications_to_insert.append((patient_id, classification, rule_used))
    
    # Insert all classifications
    cursor.executemany(
        '''INSERT OR IGNORE INTO patient_classifications 
           (patient_id, classification_level, rule_applied_id)
           VALUES (?, ?, ?)''',
        classifications_to_insert
    )
    
    conn.commit()
    
    # Show summary
    cursor.execute('''
        SELECT classification_level, COUNT(*) as count
        FROM patient_classifications
        GROUP BY classification_level
        ORDER BY count DESC
    ''')
    
    results = cursor.fetchall()
    print("✅ Classification Summary:")
    for level, count in results:
        percentage = (count / len(patients)) * 100
        print(f"   - {level}: {count} patients ({percentage:.1f}%)")

# ============================================================================
# STEP 3: DISPLAY SAMPLE DATA
# ============================================================================

def show_sample_data(conn):
    """Display some sample records"""
    print("\n📋 SAMPLE DATA (First 10 patients):\n")
    
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            p.patient_id,
            p.patient_name,
            p.age,
            p.ward,
            p.heart_rate,
            p.oxygen_saturation,
            p.diagnosis,
            pc.classification_level
        FROM patients p
        LEFT JOIN patient_classifications pc ON p.patient_id = pc.patient_id
        LIMIT 10
    ''')
    
    rows = cursor.fetchall()
    
    # Print header
    print(f"{'ID':<4} {'Name':<15} {'Age':<4} {'Ward':<15} {'HR':<4} {'O2%':<4} {'Diagnosis':<20} {'Class':<10}")
    print("="*90)
    
    # Print data
    for row in rows:
        pid, name, age, ward, hr, o2, diagnosis, classification = row
        print(f"{pid:<4} {name:<15} {age:<4} {ward:<15} {hr:<4} {o2:<4} {diagnosis:<20} {classification:<10}")

def show_statistics(conn):
    """Show database statistics"""
    print("\n📊 DATABASE STATISTICS:\n")
    
    cursor = conn.cursor()
    
    # Patient count
    cursor.execute('SELECT COUNT(*) FROM patients')
    patient_count = cursor.fetchone()[0]
    print(f"✓ Total Patients: {patient_count}")
    
    # Users count
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    print(f"✓ Total Users: {user_count}")
    
    # Rules count
    cursor.execute('SELECT COUNT(*) FROM classification_rules')
    rules_count = cursor.fetchone()[0]
    print(f"✓ Total Rules: {rules_count}")
    
    # Patients by ward
    print("\n✓ Patients by Ward:")
    cursor.execute('SELECT ward, COUNT(*) as count FROM patients GROUP BY ward ORDER BY count DESC')
    for ward, count in cursor.fetchall():
        print(f"   - {ward}: {count}")
    
    # Patients by classification
    print("\n✓ Patients by Classification:")
    cursor.execute('''
        SELECT classification_level, COUNT(*) as count 
        FROM patient_classifications 
        GROUP BY classification_level 
        ORDER BY count DESC
    ''')
    for classification, count in cursor.fetchall():
        print(f"   - {classification}: {count}")

# ============================================================================
# STEP 4: MAIN FUNCTION - RUN EVERYTHING
# ============================================================================

def main():
    """Main function - run all steps"""
    
    print("\n" + "="*60)
    print("🏥 SQLite3 Database Setup & Data Generation")
    print("="*60)
    
    # Step 1: Create database
    conn = create_database()
    
    # Step 2: Load data
    load_users(conn)
    load_rules(conn)
    load_patients(conn, num_patients=100)  # Change 100 to any number you want
    auto_classify_patients(conn)
    
    # Step 3: Show results
    show_sample_data(conn)
    show_statistics(conn)
    
    # Close connection
    conn.close()
    
    print("\n" + "="*60)
    print("✅ SUCCESS! Database ready to use")
    print("="*60)
    print("\n📁 File created: patient_db.sqlite3")
    print("\n💡 Next: Use this database in your Flask app!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()