import sqlite3
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lifelink.db")

def get_connection():
    """Get sqlite connection with dictionary access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL, -- 'donor', 'hospital', 'blood_bank', 'admin'
        status TEXT DEFAULT 'ACTIVE',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. DONORS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        city TEXT NOT NULL,
        area TEXT,
        last_donation TEXT,
        availability TEXT DEFAULT 'AVAILABLE', -- 'AVAILABLE', 'UNAVAILABLE'
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    )
    """)

    # 3. HOSPITALS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hospitals (
        hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        hospital_name TEXT NOT NULL,
        license_number TEXT NOT NULL,
        hospital_type TEXT,
        address TEXT,
        city TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT NOT NULL,
        emergency_contact TEXT,
        verification_status TEXT DEFAULT 'PENDING', -- 'PENDING', 'VERIFIED', 'REJECTED'
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    )
    """)

    # 4. BLOOD_BANKS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blood_banks (
        blood_bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        license_number TEXT,
        address TEXT,
        city TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT NOT NULL,
        verification_status TEXT DEFAULT 'VERIFIED',
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    )
    """)

    # 5. BLOOD_REQUESTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blood_requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_id INTEGER NOT NULL,
        patient_reference TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        units_required INTEGER NOT NULL,
        priority TEXT NOT NULL, -- 'CRITICAL', 'URGENT', 'NORMAL'
        required_date TEXT NOT NULL,
        location TEXT NOT NULL,
        contact_dept TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'ACTIVE', -- 'ACTIVE', 'FULFILLED', 'CANCELLED', 'EXPIRED'
        FOREIGN KEY (hospital_id) REFERENCES hospitals (hospital_id)
    )
    """)

    # 6. DONOR_RESPONSES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donor_responses (
        response_id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER NOT NULL,
        donor_id INTEGER NOT NULL,
        response_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'INTERESTED', -- 'INTERESTED', 'ACCEPTED', 'CONTACTED', 'DECLINED', 'COMPLETED'
        FOREIGN KEY (request_id) REFERENCES blood_requests (request_id),
        FOREIGN KEY (donor_id) REFERENCES donors (donor_id)
    )
    """)

    # 7. DONATIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        hospital_id INTEGER,
        request_id INTEGER,
        donation_date TEXT NOT NULL,
        units INTEGER DEFAULT 1,
        FOREIGN KEY (donor_id) REFERENCES donors (donor_id),
        FOREIGN KEY (hospital_id) REFERENCES hospitals (hospital_id),
        FOREIGN KEY (request_id) REFERENCES blood_requests (request_id)
    )
    """)

    # 8. BLOOD_INVENTORY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blood_inventory (
        unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_bank_id INTEGER NOT NULL,
        donor_id INTEGER,
        blood_group TEXT NOT NULL,
        units INTEGER DEFAULT 1,
        collection_date TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        status TEXT DEFAULT 'AVAILABLE', -- 'AVAILABLE', 'RESERVED', 'EXPIRED', 'USED'
        FOREIGN KEY (blood_bank_id) REFERENCES blood_banks (blood_bank_id)
    )
    """)

    # 9. NOTIFICATIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        request_id INTEGER,
        title TEXT,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        read_status INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)

    conn.commit()
    conn.close()

# --- USER AUTHENTICATION & PROFILE OPERATIONS ---

def create_user(email: str, password_hash: str, role: str) -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)", (email.lower().strip(), password_hash, role))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email: str) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# --- DONOR OPERATIONS ---

def create_donor(user_id: int, name: str, blood_group: str, age: int, gender: str, phone: str, city: str, area: str, last_donation: str = "") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donors (user_id, name, blood_group, age, gender, phone, city, area, last_donation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, name, blood_group, age, gender, phone, city, area, last_donation))
    conn.commit()
    donor_id = cursor.lastrowid
    conn.close()
    return donor_id

def get_donor_by_user_id(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_donor_profile(donor_id: int, name: str, phone: str, city: str, area: str, last_donation: str, availability: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE donors 
        SET name = ?, phone = ?, city = ?, area = ?, last_donation = ?, availability = ?
        WHERE donor_id = ?
    """, (name, phone, city, area, last_donation, availability, donor_id))
    conn.commit()
    conn.close()

def get_all_donors() -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- HOSPITAL OPERATIONS ---

def create_hospital(user_id: int, hospital_name: str, license_number: str, hospital_type: str, address: str, city: str, contact_person: str, phone: str, emergency_contact: str, verification_status: str = "PENDING") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hospitals (user_id, hospital_name, license_number, hospital_type, address, city, contact_person, phone, emergency_contact, verification_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, hospital_name, license_number, hospital_type, address, city, contact_person, phone, emergency_contact, verification_status))
    conn.commit()
    hospital_id = cursor.lastrowid
    conn.close()
    return hospital_id

def get_hospital_by_user_id(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_hospital_verification(hospital_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE hospitals SET verification_status = ? WHERE hospital_id = ?", (status, hospital_id))
    conn.commit()
    conn.close()

def get_all_hospitals() -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospitals")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- BLOOD BANK OPERATIONS ---

def create_blood_bank(user_id: int, name: str, license_number: str, address: str, city: str, contact_person: str, phone: str, verification_status: str = "VERIFIED") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO blood_banks (user_id, name, license_number, address, city, contact_person, phone, verification_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, name, license_number, address, city, contact_person, phone, verification_status))
    conn.commit()
    bb_id = cursor.lastrowid
    conn.close()
    return bb_id

def get_blood_bank_by_user_id(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blood_banks WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_blood_banks() -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blood_banks")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- BLOOD REQUEST OPERATIONS ---

def create_blood_request(hospital_id: int, patient_reference: str, blood_group: str, units_required: int, priority: str, required_date: str, location: str, contact_dept: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO blood_requests (hospital_id, patient_reference, blood_group, units_required, priority, required_date, location, contact_dept, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE')
    """, (hospital_id, patient_reference, blood_group, units_required, priority, required_date, location, contact_dept))
    conn.commit()
    req_id = cursor.lastrowid
    conn.close()
    return req_id

def get_all_active_requests(priority_filter: Optional[str] = None) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT r.*, h.hospital_name, h.city as hospital_city, h.phone as hospital_phone
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        WHERE r.status = 'ACTIVE'
    """
    params = []
    if priority_filter and priority_filter.upper() != "ALL":
        query += " AND UPPER(r.priority) = ?"
        params.append(priority_filter.upper())
    
    query += " ORDER BY CASE r.priority WHEN 'CRITICAL' THEN 1 WHEN 'URGENT' THEN 2 ELSE 3 END, r.created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_requests_by_hospital(hospital_id: int) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, 
            (SELECT COUNT(*) FROM donor_responses dr WHERE dr.request_id = r.request_id) as response_count
        FROM blood_requests r
        WHERE r.hospital_id = ?
        ORDER BY r.created_at DESC
    """, (hospital_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_request_status(request_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE blood_requests SET status = ? WHERE request_id = ?", (status, request_id))
    conn.commit()
    conn.close()

def get_request_by_id(request_id: int) -> Optional[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, h.hospital_name, h.city as hospital_city, h.phone as hospital_phone
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        WHERE r.request_id = ?
    """, (request_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# --- DONOR RESPONSE OPERATIONS ---

def submit_donor_response(request_id: int, donor_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    # Check if already responded
    cursor.execute("SELECT * FROM donor_responses WHERE request_id = ? AND donor_id = ?", (request_id, donor_id))
    if cursor.fetchone():
        conn.close()
        return False
    
    cursor.execute("INSERT INTO donor_responses (request_id, donor_id, status) VALUES (?, ?, 'INTERESTED')", (request_id, donor_id))
    conn.commit()
    conn.close()
    return True

def get_responses_for_request(request_id: int) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dr.*, d.name as donor_name, d.blood_group, d.phone, d.city, d.last_donation, d.user_id as donor_user_id
        FROM donor_responses dr
        JOIN donors d ON dr.donor_id = d.donor_id
        WHERE dr.request_id = ?
        ORDER BY dr.response_date DESC
    """, (request_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_responses_by_donor(donor_id: int) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dr.*, r.patient_reference, r.blood_group as req_blood_group, r.priority, r.location, r.required_date, h.hospital_name
        FROM donor_responses dr
        JOIN blood_requests r ON dr.request_id = r.request_id
        JOIN hospitals h ON r.hospital_id = h.hospital_id
        WHERE dr.donor_id = ?
        ORDER BY dr.response_date DESC
    """, (donor_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_response_status(response_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE donor_responses SET status = ? WHERE response_id = ?", (status, response_id))
    conn.commit()
    conn.close()

# --- DONATION RECORD OPERATIONS ---

def record_donation(donor_id: int, hospital_id: int, request_id: int, units: int = 1, donation_date: str = ""):
    if not donation_date:
        donation_date = datetime.now().strftime("%Y-%m-%d")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donations (donor_id, hospital_id, request_id, donation_date, units)
        VALUES (?, ?, ?, ?, ?)
    """, (donor_id, hospital_id, request_id, donation_date, units))
    
    # Update donor's last donation date
    cursor.execute("UPDATE donors SET last_donation = ? WHERE donor_id = ?", (donation_date, donor_id))
    conn.commit()
    conn.close()

def get_donations_by_donor(donor_id: int) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.*, h.hospital_name 
        FROM donations d
        LEFT JOIN hospitals h ON d.hospital_id = h.hospital_id
        WHERE d.donor_id = ?
        ORDER BY d.donation_date DESC
    """, (donor_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- BLOOD INVENTORY OPERATIONS ---

def add_blood_inventory(blood_bank_id: int, blood_group: str, units: int, collection_date: str, expiry_date: str, donor_id: Optional[int] = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO blood_inventory (blood_bank_id, donor_id, blood_group, units, collection_date, expiry_date, status)
        VALUES (?, ?, ?, ?, ?, ?, 'AVAILABLE')
    """, (blood_bank_id, donor_id, blood_group, units, collection_date, expiry_date))
    conn.commit()
    unit_id = cursor.lastrowid
    conn.close()
    return unit_id

def get_inventory_summary(blood_bank_id: Optional[int] = None) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT blood_group, SUM(units) as total_units
        FROM blood_inventory
        WHERE status = 'AVAILABLE'
    """
    params = []
    if blood_bank_id:
        query += " AND blood_bank_id = ?"
        params.append(blood_bank_id)
    
    query += " GROUP BY blood_group"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_inventory_items(blood_bank_id: Optional[int] = None) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT i.*, bb.name as blood_bank_name
        FROM blood_inventory i
        JOIN blood_banks bb ON i.blood_bank_id = bb.blood_bank_id
        WHERE 1=1
    """
    params = []
    if blood_bank_id:
        query += " AND i.blood_bank_id = ?"
        params.append(blood_bank_id)
    
    query += " ORDER BY i.expiry_date ASC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- NOTIFICATION OPERATIONS ---

def create_notification(user_id: int, title: str, message: str, request_id: Optional[int] = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (user_id, request_id, title, message)
        VALUES (?, ?, ?, ?)
    """, (user_id, request_id, title, message))
    conn.commit()
    conn.close()

def get_user_notifications(user_id: int) -> List[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM notifications 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_notification_as_read(notification_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET read_status = 1 WHERE notification_id = ?", (notification_id,))
    conn.commit()
    conn.close()

# --- SYSTEM STATS FOR DASHBOARDS ---

def get_system_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM donors WHERE availability = 'AVAILABLE'")
    available_donors = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM blood_requests WHERE status = 'ACTIVE'")
    active_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM blood_requests WHERE status = 'ACTIVE' AND priority = 'CRITICAL'")
    critical_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM blood_requests WHERE status = 'FULFILLED'")
    fulfilled_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(units), 0) FROM blood_inventory WHERE status = 'AVAILABLE'")
    total_blood_units = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hospitals WHERE verification_status = 'VERIFIED'")
    verified_hospitals = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hospitals WHERE verification_status = 'PENDING'")
    pending_hospitals = cursor.fetchone()[0]

    conn.close()
    return {
        "total_donors": total_donors,
        "available_donors": available_donors,
        "active_requests": active_requests,
        "critical_requests": critical_requests,
        "fulfilled_requests": fulfilled_requests,
        "total_blood_units": total_blood_units,
        "verified_hospitals": verified_hospitals,
        "pending_hospitals": pending_hospitals
    }
