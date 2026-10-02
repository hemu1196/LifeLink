from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.all_models import User, Donor, Hospital, BloodBank
from backend.app.schemas.schemas import UserRegister, UserLogin, Token
from backend.app.security.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=Token)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    email_clean = payload.email.lower().strip()
    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email address is already registered.")

    hashed_pwd = hash_password(payload.password)
    user = User(email=email_clean, hashed_password=hashed_pwd, role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)

    profile_dict = {}

    if payload.role == "donor":
        donor = Donor(
            user_id=user.id,
            name=payload.name or "New Donor",
            blood_group=payload.blood_group or "O+",
            age=payload.age or 25,
            gender=payload.gender or "Male",
            phone=payload.phone or "",
            city=payload.city or "Coimbatore",
            area=payload.area or "Peelamedu"
        )
        db.add(donor)
        db.commit()
        db.refresh(donor)
        profile_dict = {"donor_id": donor.id, "name": donor.name, "blood_group": donor.blood_group, "city": donor.city}

    elif payload.role == "hospital":
        hospital = Hospital(
            user_id=user.id,
            hospital_name=payload.name or "Hospital Clinic",
            license_number=payload.license_number or "LIC-GEN-100",
            hospital_type=payload.hospital_type or "Multispecialty",
            address=payload.address or "",
            city=payload.city or "Coimbatore",
            contact_person=payload.contact_person or "",
            phone=payload.phone or "",
            emergency_contact=payload.emergency_contact or "",
            verification_status="PENDING"
        )
        db.add(hospital)
        db.commit()
        db.refresh(hospital)
        profile_dict = {"hospital_id": hospital.id, "hospital_name": hospital.hospital_name, "license_number": hospital.license_number, "verification_status": hospital.verification_status}

    elif payload.role == "blood_bank":
        bb = BloodBank(
            user_id=user.id,
            name=payload.name or "Central Blood Bank",
            license_number=payload.license_number or "BB-LIC-100",
            address=payload.address or "",
            city=payload.city or "Coimbatore",
            contact_person=payload.contact_person or "",
            phone=payload.phone or "",
            verification_status="VERIFIED"
        )
        db.add(bb)
        db.commit()
        db.refresh(bb)
        profile_dict = {"blood_bank_id": bb.id, "name": bb.name, "city": bb.city}

    token_str = create_access_token({"user_id": user.id, "role": user.role, "email": user.email})
    return {
        "access_token": token_str,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id,
        "email": user.email,
        "profile": profile_dict
    }

@router.post("/login", response_model=Token)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    email_clean = payload.email.lower().strip()
    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email address or password.")

    if user.role != payload.role and user.role != "admin":
        raise HTTPException(status_code=400, detail=f"Account role is '{user.role}'. Please select the correct login tab.")

    profile_dict = {}
    if user.role == "donor":
        d = db.query(Donor).filter(Donor.user_id == user.id).first()
        if d:
            profile_dict = {"donor_id": d.id, "name": d.name, "blood_group": d.blood_group, "city": d.city, "last_donation": d.last_donation, "availability": d.availability}
    elif user.role == "hospital":
        h = db.query(Hospital).filter(Hospital.user_id == user.id).first()
        if h:
            profile_dict = {"hospital_id": h.id, "hospital_name": h.hospital_name, "license_number": h.license_number, "verification_status": h.verification_status, "city": h.city}
    elif user.role == "blood_bank":
        bb = db.query(BloodBank).filter(BloodBank.user_id == user.id).first()
        if bb:
            profile_dict = {"blood_bank_id": bb.id, "name": bb.name, "city": bb.city}
    elif user.role == "admin":
        profile_dict = {"name": "System Administrator"}

    token_str = create_access_token({"user_id": user.id, "role": user.role, "email": user.email})
    return {
        "access_token": token_str,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id,
        "email": user.email,
        "profile": profile_dict
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile_dict = {}
    if current_user.role == "donor":
        d = db.query(Donor).filter(Donor.user_id == current_user.id).first()
        if d:
            profile_dict = {"donor_id": d.id, "name": d.name, "blood_group": d.blood_group, "city": d.city, "phone": d.phone, "last_donation": d.last_donation, "availability": d.availability}
    elif current_user.role == "hospital":
        h = db.query(Hospital).filter(Hospital.user_id == current_user.id).first()
        if h:
            profile_dict = {"hospital_id": h.id, "hospital_name": h.hospital_name, "license_number": h.license_number, "verification_status": h.verification_status, "city": h.city}
    elif current_user.role == "blood_bank":
        bb = db.query(BloodBank).filter(BloodBank.user_id == current_user.id).first()
        if bb:
            profile_dict = {"blood_bank_id": bb.id, "name": bb.name, "city": bb.city}
    elif current_user.role == "admin":
        profile_dict = {"name": "System Administrator"}

    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "profile": profile_dict
    }
