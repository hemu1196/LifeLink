from datetime import datetime, timedelta
from backend.app.database import engine, Base, SessionLocal
from backend.app.models.all_models import (
    User, Donor, Hospital, BloodBank, BloodRequest, DonorResponse, Donation, BloodInventory, Notification
)
from backend.app.security.auth import hash_password

def seed_backend_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(User).count() > 0:
        print("Backend DB already seeded.")
        db.close()
        return

    print("Seeding backend database...")

    # 1. ADMIN USER
    admin_user = User(email="admin@lifelink.com", hashed_password=hash_password("admin123"), role="admin")
    db.add(admin_user)
    db.commit()

    # 2. HOSPITALS
    h1_user = User(email="cityhospital@gmail.com", hashed_password=hash_password("hospital123"), role="hospital")
    h2_user = User(email="abcmedical@gmail.com", hashed_password=hash_password("hospital123"), role="hospital")
    h3_user = User(email="ghcoimbatore@gmail.com", hashed_password=hash_password("hospital123"), role="hospital")
    h4_user = User(email="kovaicare@gmail.com", hashed_password=hash_password("hospital123"), role="hospital")

    db.add_all([h1_user, h2_user, h3_user, h4_user])
    db.commit()

    h1 = Hospital(
        user_id=h1_user.id, hospital_name="City Hospital", license_number="LIC-CBE-9842",
        hospital_type="Multispecialty", address="104 Avinashi Road, Peelamedu", city="Coimbatore",
        contact_person="Dr. Rajesh Kumar", phone="+91 98765 43210", emergency_contact="+91 98765 43211",
        verification_status="VERIFIED"
    )
    h2 = Hospital(
        user_id=h2_user.id, hospital_name="ABC Medical Center", license_number="LIC-CBE-4412",
        hospital_type="Super Specialty", address="45 Trichy Road, Singanallur", city="Coimbatore",
        contact_person="Dr. Anita Sharma", phone="+91 98421 11223", emergency_contact="+91 98421 11224",
        verification_status="VERIFIED"
    )
    h3 = Hospital(
        user_id=h3_user.id, hospital_name="GH Hospital", license_number="LIC-GOV-1002",
        hospital_type="Government Hospital", address="Collectorate Compound, RS Puram", city="Coimbatore",
        contact_person="Dr. S. Sundaram", phone="+91 94433 99887", emergency_contact="+91 94433 99888",
        verification_status="VERIFIED"
    )
    h4 = Hospital(
        user_id=h4_user.id, hospital_name="Kovai Care Hospital", license_number="LIC-CBE-7789",
        hospital_type="General Hospital", address="12 Gandhipuram 4th Street", city="Coimbatore",
        contact_person="Dr. Meena Ramesh", phone="+91 97890 12345", emergency_contact="+91 97890 54321",
        verification_status="PENDING"
    )

    db.add_all([h1, h2, h3, h4])
    db.commit()

    # 3. BLOOD BANKS
    bb1_user = User(email="cbebloodbank@gmail.com", hashed_password=hash_password("bloodbank123"), role="blood_bank")
    bb2_user = User(email="apexblood@gmail.com", hashed_password=hash_password("bloodbank123"), role="blood_bank")
    db.add_all([bb1_user, bb2_user])
    db.commit()

    bb1 = BloodBank(
        user_id=bb1_user.id, name="Coimbatore Central Blood Bank", license_number="BB-CBE-001",
        address="88 Crosscut Road, Gandhipuram", city="Coimbatore", contact_person="K. Vasanth",
        phone="+91 91234 56789", verification_status="VERIFIED"
    )
    bb2 = BloodBank(
        user_id=bb2_user.id, name="Apex Blood Trust", license_number="BB-CBE-008",
        address="22 Race Course Road", city="Coimbatore", contact_person="S. Priya",
        phone="+91 93456 78901", verification_status="VERIFIED"
    )
    db.add_all([bb1, bb2])
    db.commit()

    # 4. DONORS
    today = datetime.now().date()
    d1_u = User(email="rahul@gmail.com", hashed_password=hash_password("donor123"), role="donor")
    d2_u = User(email="arun@gmail.com", hashed_password=hash_password("donor123"), role="donor")
    d3_u = User(email="kiran@gmail.com", hashed_password=hash_password("donor123"), role="donor")
    d4_u = User(email="naveen@gmail.com", hashed_password=hash_password("donor123"), role="donor")
    d5_u = User(email="priya@gmail.com", hashed_password=hash_password("donor123"), role="donor")

    db.add_all([d1_u, d2_u, d3_u, d4_u, d5_u])
    db.commit()

    d1 = Donor(user_id=d1_u.id, name="Rahul Verma", blood_group="O-", age=26, gender="Male", phone="+91 98111 22334", city="Coimbatore", area="Peelamedu", last_donation=(today - timedelta(days=120)).strftime("%Y-%m-%d"))
    d2 = Donor(user_id=d2_u.id, name="Arun Kumar", blood_group="O-", age=31, gender="Male", phone="+91 98222 33445", city="Coimbatore", area="Gandhipuram", last_donation=(today - timedelta(days=105)).strftime("%Y-%m-%d"))
    d3 = Donor(user_id=d3_u.id, name="Kiran Reddy", blood_group="B+", age=29, gender="Male", phone="+91 98333 44556", city="Coimbatore", area="RS Puram", last_donation=(today - timedelta(days=95)).strftime("%Y-%m-%d"))
    d4 = Donor(user_id=d4_u.id, name="Naveen Prakash", blood_group="A+", age=24, gender="Male", phone="+91 98444 55667", city="Coimbatore", area="Peelamedu", last_donation=(today - timedelta(days=150)).strftime("%Y-%m-%d"))
    d5 = Donor(user_id=d5_u.id, name="Priya Sundar", blood_group="AB-", age=28, gender="Female", phone="+91 98555 66778", city="Coimbatore", area="Singanallur", last_donation=(today - timedelta(days=110)).strftime("%Y-%m-%d"))

    db.add_all([d1, d2, d3, d4, d5])
    db.commit()

    # 5. EMERGENCY REQUESTS
    r1 = BloodRequest(
        hospital_id=h1.id, patient_reference="PT1025", blood_group="O-", units_required=3, priority="CRITICAL",
        required_date=today.strftime("%Y-%m-%d") + " 11:30 PM", location="Peelamedu, Coimbatore",
        contact_dept="Emergency Department (+91 98765 43211)", status="ACTIVE"
    )
    r2 = BloodRequest(
        hospital_id=h2.id, patient_reference="PT1089", blood_group="B+", units_required=2, priority="URGENT",
        required_date=(today + timedelta(days=1)).strftime("%Y-%m-%d") + " 06:00 PM", location="Singanallur, Coimbatore",
        contact_dept="ICU Ward 3 (+91 98421 11224)", status="ACTIVE"
    )
    r3 = BloodRequest(
        hospital_id=h3.id, patient_reference="PT2014", blood_group="A+", units_required=1, priority="NORMAL",
        required_date=(today + timedelta(days=2)).strftime("%Y-%m-%d") + " 10:00 AM", location="RS Puram, Coimbatore",
        contact_dept="Blood Transfusion Desk", status="ACTIVE"
    )
    db.add_all([r1, r2, r3])
    db.commit()

    # 6. DONOR RESPONSES
    dr1 = DonorResponse(request_id=r1.id, donor_id=d1.id, status="INTERESTED")
    dr2 = DonorResponse(request_id=r1.id, donor_id=d2.id, status="INTERESTED")
    dr3 = DonorResponse(request_id=r2.id, donor_id=d3.id, status="INTERESTED")
    db.add_all([dr1, dr2, dr3])
    db.commit()

    # 7. INVENTORY
    inv1 = BloodInventory(blood_bank_id=bb1.id, blood_group="O-", units=2, collection_date=(today - timedelta(days=5)).strftime("%Y-%m-%d"), expiry_date=(today + timedelta(days=30)).strftime("%Y-%m-%d"), status="AVAILABLE")
    inv2 = BloodInventory(blood_bank_id=bb1.id, blood_group="O+", units=14, collection_date=(today - timedelta(days=10)).strftime("%Y-%m-%d"), expiry_date=(today + timedelta(days=25)).strftime("%Y-%m-%d"), status="AVAILABLE")
    inv3 = BloodInventory(blood_bank_id=bb1.id, blood_group="A+", units=12, collection_date=(today - timedelta(days=4)).strftime("%Y-%m-%d"), expiry_date=(today + timedelta(days=31)).strftime("%Y-%m-%d"), status="AVAILABLE")
    inv4 = BloodInventory(blood_bank_id=bb1.id, blood_group="B+", units=8, collection_date=(today - timedelta(days=2)).strftime("%Y-%m-%d"), expiry_date=(today + timedelta(days=33)).strftime("%Y-%m-%d"), status="AVAILABLE")
    inv5 = BloodInventory(blood_bank_id=bb2.id, blood_group="O-", units=1, collection_date=(today - timedelta(days=1)).strftime("%Y-%m-%d"), expiry_date=(today + timedelta(days=34)).strftime("%Y-%m-%d"), status="AVAILABLE")
    db.add_all([inv1, inv2, inv3, inv4, inv5])
    db.commit()

    # 8. NOTIFICATIONS
    n1 = Notification(user_id=d1_u.id, request_id=r1.id, title="🚨 Emergency O- Requirement", message="City Hospital posted a Critical O- requirement near Peelamedu.")
    n2 = Notification(user_id=h1_user.id, request_id=r1.id, title="❤️ New Donor Response", message="Rahul Verma (O-) responded 'I Can Donate' to request PT1025.")
    db.add_all([n1, n2])
    db.commit()

    print("Backend database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_backend_db()
