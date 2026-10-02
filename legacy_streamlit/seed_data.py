import os
from datetime import datetime, timedelta
from database import (
    init_db, create_user, create_donor, create_hospital, create_blood_bank,
    create_blood_request, submit_donor_response, record_donation, add_blood_inventory,
    create_notification, get_connection
)
from utils.helpers import hash_password

def seed_database():
    """Populate database with rich sample data for demonstration."""
    init_db()

    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()

    if count > 0:
        print("Database already populated.")
        return

    print("Seeding database with sample demo data...")

    # 1. ADMIN USER
    admin_uid = create_user("admin@lifelink.com", hash_password("admin123"), "admin")

    # 2. HOSPITALS
    # Hospital 1: City Hospital (Verified)
    h1_uid = create_user("cityhospital@gmail.com", hash_password("hospital123"), "hospital")
    h1_id = create_hospital(
        user_id=h1_uid,
        hospital_name="City Hospital",
        license_number="LIC-CBE-9842",
        hospital_type="Multispecialty",
        address="104 Avinashi Road, Peelamedu",
        city="Coimbatore",
        contact_person="Dr. Rajesh Kumar",
        phone="+91 98765 43210",
        emergency_contact="+91 98765 43211",
        verification_status="VERIFIED"
    )

    # Hospital 2: ABC Medical Center (Verified)
    h2_uid = create_user("abcmedical@gmail.com", hash_password("hospital123"), "hospital")
    h2_id = create_hospital(
        user_id=h2_uid,
        hospital_name="ABC Medical Center",
        license_number="LIC-CBE-4412",
        hospital_type="Super Specialty",
        address="45 Trichy Road, Singanallur",
        city="Coimbatore",
        contact_person="Dr. Anita Sharma",
        phone="+91 98421 11223",
        emergency_contact="+91 98421 11224",
        verification_status="VERIFIED"
    )

    # Hospital 3: GH Hospital (Verified)
    h3_uid = create_user("ghcoimbatore@gmail.com", hash_password("hospital123"), "hospital")
    h3_id = create_hospital(
        user_id=h3_uid,
        hospital_name="GH Hospital",
        license_number="LIC-GOV-1002",
        hospital_type="Government Hospital",
        address="Collectorate Compound, RS Puram",
        city="Coimbatore",
        contact_person="Dr. S. Sundaram",
        phone="+91 94433 99887",
        emergency_contact="+91 94433 99888",
        verification_status="VERIFIED"
    )

    # Hospital 4: Kovai Care Hospital (Pending Verification)
    h4_uid = create_user("kovaicare@gmail.com", hash_password("hospital123"), "hospital")
    h4_id = create_hospital(
        user_id=h4_uid,
        hospital_name="Kovai Care Hospital",
        license_number="LIC-CBE-7789",
        hospital_type="General Hospital",
        address="12 Gandhipuram 4th Street",
        city="Coimbatore",
        contact_person="Dr. Meena Ramesh",
        phone="+91 97890 12345",
        emergency_contact="+91 97890 54321",
        verification_status="PENDING"
    )

    # 3. BLOOD BANKS
    bb1_uid = create_user("cbebloodbank@gmail.com", hash_password("bloodbank123"), "blood_bank")
    bb1_id = create_blood_bank(
        user_id=bb1_uid,
        name="Coimbatore Central Blood Bank",
        license_number="BB-CBE-001",
        address="88 Crosscut Road, Gandhipuram",
        city="Coimbatore",
        contact_person="K. Vasanth",
        phone="+91 91234 56789",
        verification_status="VERIFIED"
    )

    bb2_uid = create_user("apexblood@gmail.com", hash_password("bloodbank123"), "blood_bank")
    bb2_id = create_blood_bank(
        user_id=bb2_uid,
        name="Apex Blood Trust",
        license_number="BB-CBE-008",
        address="22 Race Course Road",
        city="Coimbatore",
        contact_person="S. Priya",
        phone="+91 93456 78901",
        verification_status="VERIFIED"
    )

    # 4. DONORS
    today = datetime.now().date()

    # Donor 1: Rahul (O-)
    d1_uid = create_user("rahul@gmail.com", hash_password("donor123"), "donor")
    d1_id = create_donor(
        user_id=d1_uid, name="Rahul Verma", blood_group="O-", age=26, gender="Male",
        phone="+91 98111 22334", city="Coimbatore", area="Peelamedu",
        last_donation=(today - timedelta(days=120)).strftime("%Y-%m-%d")
    )

    # Donor 2: Arun (O-)
    d2_uid = create_user("arun@gmail.com", hash_password("donor123"), "donor")
    d2_id = create_donor(
        user_id=d2_uid, name="Arun Kumar", blood_group="O-", age=31, gender="Male",
        phone="+91 98222 33445", city="Coimbatore", area="Gandhipuram",
        last_donation=(today - timedelta(days=105)).strftime("%Y-%m-%d")
    )

    # Donor 3: Kiran (B+)
    d3_uid = create_user("kiran@gmail.com", hash_password("donor123"), "donor")
    d3_id = create_donor(
        user_id=d3_uid, name="Kiran Reddy", blood_group="B+", age=29, gender="Male",
        phone="+91 98333 44556", city="Coimbatore", area="RS Puram",
        last_donation=(today - timedelta(days=95)).strftime("%Y-%m-%d")
    )

    # Donor 4: Naveen (A+)
    d4_uid = create_user("naveen@gmail.com", hash_password("donor123"), "donor")
    d4_id = create_donor(
        user_id=d4_uid, name="Naveen Prakash", blood_group="A+", age=24, gender="Male",
        phone="+91 98444 55667", city="Coimbatore", area="Peelamedu",
        last_donation=(today - timedelta(days=150)).strftime("%Y-%m-%d")
    )

    # Donor 5: Priya (AB-)
    d5_uid = create_user("priya@gmail.com", hash_password("donor123"), "donor")
    d5_id = create_donor(
        user_id=d5_uid, name="Priya Sundar", blood_group="AB-", age=28, gender="Female",
        phone="+91 98555 66778", city="Coimbatore", area="Singanallur",
        last_donation=(today - timedelta(days=110)).strftime("%Y-%m-%d")
    )

    # Donor 6: Deepa (O+) - Ineligible (donated 30 days ago)
    d6_uid = create_user("deepa@gmail.com", hash_password("donor123"), "donor")
    d6_id = create_donor(
        user_id=d6_uid, name="Deepa Nair", blood_group="O+", age=33, gender="Female",
        phone="+91 98666 77889", city="Coimbatore", area="RS Puram",
        last_donation=(today - timedelta(days=30)).strftime("%Y-%m-%d")
    )

    # 5. EMERGENCY BLOOD REQUESTS
    # Request 1: CRITICAL O- at City Hospital
    r1_id = create_blood_request(
        hospital_id=h1_id,
        patient_reference="PT1025",
        blood_group="O-",
        units_required=3,
        priority="CRITICAL",
        required_date=today.strftime("%Y-%m-%d") + " 11:30 PM",
        location="Peelamedu, Coimbatore",
        contact_dept="Emergency Department (+91 98765 43211)"
    )

    # Request 2: URGENT B+ at ABC Medical Center
    r2_id = create_blood_request(
        hospital_id=h2_id,
        patient_reference="PT1089",
        blood_group="B+",
        units_required=2,
        priority="URGENT",
        required_date=(today + timedelta(days=1)).strftime("%Y-%m-%d") + " 06:00 PM",
        location="Singanallur, Coimbatore",
        contact_dept="ICU Ward 3 (+91 98421 11224)"
    )

    # Request 3: NORMAL A+ at GH Hospital
    r3_id = create_blood_request(
        hospital_id=h3_id,
        patient_reference="PT2014",
        blood_group="A+",
        units_required=1,
        priority="NORMAL",
        required_date=(today + timedelta(days=2)).strftime("%Y-%m-%d") + " 10:00 AM",
        location="RS Puram, Coimbatore",
        contact_dept="Blood Transfusion Desk"
    )

    # 6. DONOR RESPONSES
    submit_donor_response(request_id=r1_id, donor_id=d1_id) # Rahul -> O- request
    submit_donor_response(request_id=r1_id, donor_id=d2_id) # Arun -> O- request
    submit_donor_response(request_id=r2_id, donor_id=d3_id) # Kiran -> B+ request

    # 7. BLOOD INVENTORY AT BLOOD BANKS
    # Central Blood Bank Stock
    add_blood_inventory(bb1_id, "O-", 2, (today - timedelta(days=5)).strftime("%Y-%m-%d"), (today + timedelta(days=30)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb1_id, "O+", 14, (today - timedelta(days=10)).strftime("%Y-%m-%d"), (today + timedelta(days=25)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb1_id, "A+", 12, (today - timedelta(days=4)).strftime("%Y-%m-%d"), (today + timedelta(days=31)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb1_id, "A-", 3, (today - timedelta(days=8)).strftime("%Y-%m-%d"), (today + timedelta(days=27)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb1_id, "B+", 8, (today - timedelta(days=2)).strftime("%Y-%m-%d"), (today + timedelta(days=33)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb1_id, "AB+", 6, (today - timedelta(days=15)).strftime("%Y-%m-%d"), (today + timedelta(days=20)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb1_id, "AB-", 1, (today - timedelta(days=25)).strftime("%Y-%m-%d"), (today + timedelta(days=10)).strftime("%Y-%m-%d"))

    # Apex Blood Trust Stock
    add_blood_inventory(bb2_id, "O-", 1, (today - timedelta(days=1)).strftime("%Y-%m-%d"), (today + timedelta(days=34)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb2_id, "B-", 2, (today - timedelta(days=7)).strftime("%Y-%m-%d"), (today + timedelta(days=28)).strftime("%Y-%m-%d"))
    add_blood_inventory(bb2_id, "A+", 8, (today - timedelta(days=3)).strftime("%Y-%m-%d"), (today + timedelta(days=32)).strftime("%Y-%m-%d"))

    # 8. COMPLETED PAST DONATIONS FOR HISTORY & ANALYTICS
    record_donation(d1_id, h1_id, r1_id, units=1, donation_date=(today - timedelta(days=120)).strftime("%Y-%m-%d"))
    record_donation(d2_id, h2_id, None, units=1, donation_date=(today - timedelta(days=105)).strftime("%Y-%m-%d"))
    record_donation(d3_id, h1_id, None, units=1, donation_date=(today - timedelta(days=95)).strftime("%Y-%m-%d"))
    record_donation(d4_id, h3_id, None, units=1, donation_date=(today - timedelta(days=150)).strftime("%Y-%m-%d"))

    # 9. NOTIFICATIONS
    create_notification(d1_uid, "🚨 Emergency O- Requirement", "City Hospital posted a Critical O- requirement near Peelamedu.", r1_id)
    create_notification(d2_uid, "🚨 Emergency O- Requirement", "City Hospital posted a Critical O- requirement near Gandhipuram.", r1_id)
    create_notification(d3_uid, "🚨 Emergency B+ Requirement", "ABC Medical Center requested 2 units of B+ blood.", r2_id)
    create_notification(h1_uid, "❤️ New Donor Response", "Rahul Verma (O-) responded 'I Can Donate' to Request PT1025.", r1_id)

    print("Sample demo data successfully seeded!")

if __name__ == "__main__":
    seed_database()
