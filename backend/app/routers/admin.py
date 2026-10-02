from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from backend.app.database import get_db
from backend.app.models.all_models import User, Donor, Hospital, BloodBank, BloodRequest, BloodInventory
from backend.app.schemas.schemas import HospitalOut, DonorOut, BloodBankOut
from backend.app.security.auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin Portal"])

def verify_admin_role(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin authorization required.")

@router.get("/stats")
def get_admin_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_admin_role(current_user)

    total_donors = db.query(Donor).count()
    available_donors = db.query(Donor).filter(Donor.availability == "AVAILABLE").count()
    active_requests = db.query(BloodRequest).filter(BloodRequest.status == "ACTIVE").count()
    critical_requests = db.query(BloodRequest).filter(BloodRequest.status == "ACTIVE", BloodRequest.priority == "CRITICAL").count()
    fulfilled_requests = db.query(BloodRequest).filter(BloodRequest.status == "FULFILLED").count()
    total_blood_units = db.query(func.sum(BloodInventory.units)).filter(BloodInventory.status == "AVAILABLE").scalar() or 0
    verified_hospitals = db.query(Hospital).filter(Hospital.verification_status == "VERIFIED").count()
    pending_hospitals = db.query(Hospital).filter(Hospital.verification_status == "PENDING").count()

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

@router.get("/hospitals", response_model=List[HospitalOut])
def get_all_hospitals(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_admin_role(current_user)
    return db.query(Hospital).order_by(Hospital.id.desc()).all()

@router.put("/hospitals/{hospital_id}/verify")
def verify_hospital(hospital_id: int, status_str: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_admin_role(current_user)

    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found.")

    hospital.verification_status = status_str.upper()
    db.commit()
    return {"message": f"Hospital '{hospital.hospital_name}' status set to {hospital.verification_status}"}

@router.get("/donors", response_model=List[DonorOut])
def get_all_donors(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_admin_role(current_user)
    return db.query(Donor).all()

@router.get("/blood-banks", response_model=List[BloodBankOut])
def get_all_blood_banks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_admin_role(current_user)
    return db.query(BloodBank).all()
