from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from backend.app.database import get_db
from backend.app.models.all_models import User, Hospital, BloodRequest, DonorResponse, Donation, Notification, Donor
from backend.app.schemas.schemas import BloodRequestCreate, BloodRequestOut, ResponseStatusUpdate
from backend.app.security.auth import get_current_user

router = APIRouter(prefix="/api/hospital", tags=["Hospital Portal"])

@router.get("/dashboard")
def get_hospital_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.user_id == current_user.id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital profile not found.")

    requests = db.query(BloodRequest).filter(BloodRequest.hospital_id == hospital.id).all()
    active_reqs = [r for r in requests if r.status == "ACTIVE"]
    critical_reqs = [r for r in active_reqs if r.priority == "CRITICAL"]
    fulfilled_reqs = [r for r in requests if r.status == "FULFILLED"]
    
    total_responses = 0
    for r in requests:
        total_responses += len(r.responses) if r.responses else 0

    return {
        "hospital_name": hospital.hospital_name,
        "verification_status": hospital.verification_status,
        "active_requests_count": len(active_reqs),
        "critical_requests_count": len(critical_reqs),
        "donors_responded_count": total_responses,
        "requests_fulfilled_count": len(fulfilled_reqs)
    }

@router.post("/requests", response_model=BloodRequestOut)
def create_request(payload: BloodRequestCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.user_id == current_user.id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital profile not found.")

    if hospital.verification_status != "VERIFIED":
        raise HTTPException(status_code=403, detail="Hospital verification is PENDING. Publishing emergency requests requires Admin verification.")

    req = BloodRequest(
        hospital_id=hospital.id,
        patient_reference=payload.patient_reference,
        blood_group=payload.blood_group,
        units_required=payload.units_required,
        priority=payload.priority,
        required_date=payload.required_date,
        location=payload.location,
        contact_dept=payload.contact_dept,
        status="ACTIVE"
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    
    req_dict = {
        "id": req.id,
        "hospital_id": req.hospital_id,
        "hospital_name": hospital.hospital_name,
        "patient_reference": req.patient_reference,
        "blood_group": req.blood_group,
        "units_required": req.units_required,
        "priority": req.priority,
        "required_date": req.required_date,
        "location": req.location,
        "contact_dept": req.contact_dept,
        "created_at": req.created_at,
        "status": req.status,
        "response_count": 0
    }
    return req_dict

@router.get("/requests", response_model=List[BloodRequestOut])
def get_hospital_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.user_id == current_user.id).first()
    if not hospital:
        return []

    requests = db.query(BloodRequest).filter(BloodRequest.hospital_id == hospital.id).order_by(BloodRequest.created_at.desc()).all()
    result = []
    for r in requests:
        result.append({
            "id": r.id,
            "hospital_id": r.hospital_id,
            "hospital_name": hospital.hospital_name,
            "patient_reference": r.patient_reference,
            "blood_group": r.blood_group,
            "units_required": r.units_required,
            "priority": r.priority,
            "required_date": r.required_date,
            "location": r.location,
            "contact_dept": r.contact_dept,
            "created_at": r.created_at,
            "status": r.status,
            "response_count": len(r.responses) if r.responses else 0
        })
    return result

@router.put("/requests/{request_id}/status")
def update_request_status(request_id: int, status_str: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.user_id == current_user.id).first()
    req = db.query(BloodRequest).filter(BloodRequest.id == request_id, BloodRequest.hospital_id == hospital.id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found.")

    req.status = status_str.upper()
    db.commit()
    return {"message": f"Request status updated to {req.status}"}

@router.get("/responses")
def get_hospital_donor_responses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.user_id == current_user.id).first()
    if not hospital:
        return []

    requests = db.query(BloodRequest).filter(BloodRequest.hospital_id == hospital.id).all()
    req_ids = [r.id for r in requests]

    responses = db.query(DonorResponse).filter(DonorResponse.request_id.in_(req_ids)).all() if req_ids else []

    out = []
    for resp in responses:
        donor = resp.donor
        req = resp.request
        out.append({
            "id": resp.id,
            "request_id": resp.request_id,
            "patient_reference": req.patient_reference if req else "",
            "donor_id": resp.donor_id,
            "donor_name": donor.name if donor else "Unknown Donor",
            "blood_group": donor.blood_group if donor else "",
            "phone": donor.phone if donor else "",
            "city": donor.city if donor else "",
            "response_date": resp.response_date,
            "status": resp.status
        })
    return out

@router.put("/responses/{response_id}/status")
def update_response_status(response_id: int, payload: ResponseStatusUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resp = db.query(DonorResponse).filter(DonorResponse.id == response_id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Donor response not found.")

    hospital = db.query(Hospital).filter(Hospital.user_id == current_user.id).first()
    resp.status = payload.status.upper()

    # If status is COMPLETED, record donation and update donor's last donation date
    if payload.status.upper() == "COMPLETED":
        today_str = datetime.now().strftime("%Y-%m-%d")
        donation = Donation(
            donor_id=resp.donor_id,
            hospital_id=hospital.id,
            request_id=resp.request_id,
            donation_date=today_str,
            units=1
        )
        db.add(donation)

        donor = db.query(Donor).filter(Donor.id == resp.donor_id).first()
        if donor:
            donor.last_donation = today_str

        # Notify donor user
        if donor and donor.user_id:
            notif = Notification(
                user_id=donor.user_id,
                title="❤️ Donation Completed",
                message=f"Thank you for donating blood at {hospital.hospital_name}!"
            )
            db.add(notif)

    elif payload.status.upper() == "ACCEPTED":
        donor = db.query(Donor).filter(Donor.id == resp.donor_id).first()
        if donor and donor.user_id:
            notif = Notification(
                user_id=donor.user_id,
                title="✅ Response Accepted!",
                message=f"{hospital.hospital_name} accepted your donation response for request {resp.request.patient_reference}."
            )
            db.add(notif)

    db.commit()
    return {"message": f"Response status updated to {resp.status}"}
