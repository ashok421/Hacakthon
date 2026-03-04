# 🏥 Patient Database Documentation

## Overview
A SQLite3 database management system for hospital patient records, designed to store patient information, vital signs, diagnoses, and automated patient classifications based on health metrics.

---

## 📊 Database Schema

### Table 1: `users`
**Purpose:** Store administrator and manager login credentials

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| username | TEXT | UNIQUE, NOT NULL | Login username |
| password | TEXT | NOT NULL | Login password |
| role | TEXT | NOT NULL | User role (Administrator, Manager) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation date |

**Sample Data:**
- Admin: `admin` / `admin123` (Administrator)
- Manager: `manager1` / `pass123` (Manager)

---

### Table 2: `patients`
**Purpose:** Store patient medical records and vital signs

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| patient_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique patient identifier |
| patient_name | TEXT | NOT NULL | Full name of patient |
| age | INTEGER | NOT NULL | Patient age |
| gender | TEXT | - | M or F |
| ward | TEXT | - | Ward assignment (ICU, Emergency, etc.) |
| doctor_assigned | TEXT | - | Assigned doctor name |
| heart_rate | INTEGER | - | Beats per minute |
| blood_pressure | TEXT | - | Format: "SYS/DIA" (e.g., "120/80") |
| temperature | REAL | - | Body temperature in Celsius |
| oxygen_saturation | INTEGER | - | SpO2 percentage (0-100) |
| diagnosis | TEXT | - | Medical diagnosis |
| admission_date | TIMESTAMP | - | Date admitted to hospital |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation date |

---

### Table 3: `classification_rules`
**Purpose:** Define rules for automatic patient classification

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| rule_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique rule identifier |
| rule_name | TEXT | UNIQUE, NOT NULL | Name of the classification rule |
| condition_type | TEXT | - | What metric to check (heart_rate, oxygen_saturation, temperature) |
| min_threshold | REAL | - | Minimum value for rule match |
| max_threshold | REAL | - | Maximum value for rule match |
| classification_level | TEXT | - | Classification category (Critical, Moderate, Stable) |
| created_by | INTEGER | FOREIGN KEY | User who created the rule |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Rule creation date |

**Built-in Rules:**

| Rule Name | Metric | Range | Level |
|-----------|--------|-------|-------|
| High Heart Rate | Heart Rate | 120-200 bpm | Critical |
| Low Oxygen | O2 Saturation | 0-89% | Critical |
| High Temperature | Temperature | 39.0-42.0°C | Critical |
| Elevated Heart Rate | Heart Rate | 100-119 bpm | Moderate |
| Borderline Oxygen | O2 Saturation | 90-94% | Moderate |
| Elevated Temperature | Temperature | 37.5-38.9°C | Moderate |
| Normal Heart Rate | Heart Rate | 60-99 bpm | Stable |
| Good Oxygen Level | O2 Saturation | 95-100% | Stable |
| Normal Temperature | Temperature | 36.0-37.4°C | Stable |

---

### Table 4: `patient_classifications`
**Purpose:** Store automatic classification results for each patient

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| classification_id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique classification record |
| patient_id | INTEGER | FOREIGN KEY | Reference to patient |
| classification_level | TEXT | - | Assigned level (Critical, Moderate, Stable) |
| rule_applied_id | INTEGER | FOREIGN KEY | Which rule was applied |
| classified_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Classification date/time |

---

## 🐍 Python Scripts

### 1. **SQLITE3_DATA.py**
**Main database setup and data generation script**

**Functions:**
- `create_database()` - Creates database file and tables
- `load_users()` - Inserts default admin and manager users
- `load_rules()` - Inserts 9 classification rules
- `load_patients()` - Generates 100 random patient records
- `auto_classify_patients()` - Automatically classifies patients based on vital signs
- `show_sample_data()` - Displays first 10 patient records
- `show_statistics()` - Shows database statistics

**Features:**
- ✅ Deletes existing database on each run (fresh start)
- ✅ Generates realistic patient data
- ✅ Automatic patient classification
- ✅ Custom datetime adapter for Python 3.12+ compatibility

**Usage:**
```bash
python SQLITE3_DATA.py
```

**Output:**
- Creates `patient_db.sqlite3`
- Displays loading progress
- Shows sample data
- Displays statistics

---

### 2. **query_all_data.py**
**Display all database records in formatted table view**

**Features:**
- ✅ Shows all data from all 4 tables
- ✅ Formatted column output
- ✅ Record counts per table
- ✅ Database statistics

**Usage:**
```bash
python query_all_data.py
```

**Output:**
- Displays all tables with formatted data
- Shows total records per table
- Pretty-printed with borders

---

### 3. **export_to_csv.py**
**Export all tables to individual CSV files**

**Features:**
- ✅ Creates separate CSV file for each table
- ✅ Includes column headers
- ✅ Preserves data types
- ✅ Progress indicators

**Usage:**
```bash
python export_to_csv.py
```

**Output Files Created:**
- `users.csv`
- `patients.csv`
- `classification_rules.csv`
- `patient_classifications.csv`

---

## 🚀 Quick Start Guide

### Step 1: Create Database and Load Data
```bash
python SQLITE3_DATA.py
```

### Step 2: View All Data
```bash
python query_all_data.py
```

### Step 3: Export to CSV
```bash
python export_to_csv.py
```

---

## 📈 Data Flow

```
┌─────────────────────────────────────┐
│   SQLITE3_DATA.py (Main Script)     │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
   Create DB    Load Data
        │             │
        └──────┬──────┘
               ▼
    Auto-classify Patients
               │
    ┌──────────┴──────────┐
    ▼                     ▼
query_all_data.py   export_to_csv.py
   (View)             (Export)
```

---

## 🔑 Key Features

### Automatic Classification
- Patients are automatically classified as **Critical**, **Moderate**, or **Stable**
- Classification is based on vital signs (heart rate, oxygen saturation, temperature)
- Critical status takes priority over other classifications

### Data Integrity
- UNIQUE constraint on username (no duplicate logins)
- FOREIGN KEY relationships between tables
- DEFAULT timestamps for audit trail
- 100 realistic patient records generated on each run

### Python 3.12+ Compatible
- Custom datetime adapters registered
- No deprecation warnings
- Proper datetime serialization to/from SQLite

---

## 📝 Sample Statistics

When you run `SQLITE3_DATA.py`, you'll get output like:

```
✅ Classification Summary:
   - Stable: 45 patients (45.0%)
   - Moderate: 35 patients (35.0%)
   - Critical: 20 patients (20.0%)

✓ Patients by Ward:
   - ICU: 25
   - Emergency: 20
   - General Ward: 22
   - Cardiology: 18
   - Respiratory: 15
```

---

## 🔒 Security Note

**Current Implementation:** Uses plain text passwords (for demo/testing only)

**Production Recommendations:**
- Hash passwords using bcrypt or argon2
- Implement proper authentication/authorization
- Use environment variables for sensitive data
- Add audit logging
- Implement role-based access control (RBAC)

---

## 📋 Database Specifications

- **Type:** SQLite3
- **File Size:** ~500KB (with 100 patient records)
- **Python Version:** 3.8+
- **Dependencies:** Only standard library (sqlite3, random, datetime, csv, os)

---

## 🆘 Troubleshooting

### "Database is locked" Error
- Close any other applications accessing the database
- Delete `patient_db.sqlite3` and run setup script again

### "No such table" Error
- Run `SQLITE3_DATA.py` first to create tables
- Check that `patient_db.sqlite3` exists in same directory

### Datetime Issues
- Update to Python 3.12+
- Scripts include custom adapters for compatibility

---

## 📞 Support

For issues or questions about the database schema and scripts, refer to the function docstrings in each Python file.

---

**Last Updated:** March 4, 2026
**Database Version:** 1.0
**Author:** Ashok Cheekati
