from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.models.all_models import User, Donor, BloodRequest, DonorResponse, Donation, Notification
from backend.app.schemas.schemas import DonorOut, DonorUpdate, DonorResponseOut
from backend.app.security.auth import get_current_user
from backend.app.services.compatibility import is_blood_compatible
from backend.app.services.eligibility import get_donor_eligibility

router = APIRouter(prefix="/api/donor", tags=["Donor Portal"])

@router.get("/profile", response_model=DonorOut)
def get_donor_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.user_id == current_user.id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor profile not found.")
    return donor

@router.put("/profile", response_model=DonorOut)
def update_donor_profile(payload: DonorUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.user_id == current_user.id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor profile not found.")

    donor.name = payload.name
    donor.phone = payload.phone
    donor.city = payload.city
    donor.area = payload.area
    donor.last_donation = payload.last_donation or ""
    donor.availability = payload.availability or "AVAILABLE"

    db.commit()
    db.refresh(donor)
    return donor

@router.post("/respond/{request_id}")
def respond_to_request(request_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.user_id == current_user.id).first()
    if not donor:
        raise HTTPException(status_code=400, detail="Only registered Donors can respond.")

    req = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    if not req or req.status != "ACTIVE":
        raise HTTPException(status_code=404, detail="Blood request not active or not found.")

    # 1. Compatibility Check
    if not is_blood_compatible(donor.blood_group, req.blood_group):
        raise HTTPException(status_code=400, detail=f"Incompatible blood group. Your group is {donor.blood_group}, but request requires {req.blood_group}.")

    # 2. Eligibility Check
    elig = get_donor_eligibility(donor.last_donation)
    if not elig["eligible"]:
        raise HTTPException(status_code=400, detail=elig["message"])

    # 3. Check Duplicate Response
    existing = db.query(DonorResponse).filter(DonorResponse.request_id == request_id, DonorResponse.donor_id == donor.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already submitted a response for this request.")

    resp = DonorResponse(request_id=request_id, donor_id=donor.id, status="INTERESTED")
    db.add(resp)

    # Notify hospital user
    if req.hospital:
        h_user_id = req.hospital.user_id
        notif = Notification(
            user_id=h_user_id,
            request_id=request_id,
            title="❤️ New Donor Response",
            message=f"Donor {donor.name} ({donor.blood_group}) responded 'I Can Donate' to request {req.patient_reference}."
        )
        db.add(notif)

    db.commit()
    return {"message": "Response submitted successfully!", "patient_reference": req.patient_reference}

@router.get("/responses", response_model=List[DonorResponseOut])
def get_donor_responses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.user_id == current_user.id).first()
    if not donor:
        return []

    responses = db.query(DonorResponse).filter(DonorResponse.donor_id == donor.id).all()
    out = []
    for r in responses:
        out.append({
            "id": r.id,
            "request_id": r.request_id,
            "donor_id": r.donor_id,
            "response_date": r.response_date,
            "status": r.status,
            "patient_reference": r.request.patient_reference if r.request else "",
            "hospital_name": r.request.hospital.hospital_name if r.request and r.request.hospital else "",
            "required_date": r.request.required_date if r.request else "",
            "location": r.request.location if r.request else ""
        })
    return out

@router.get("/donations")
def get_donor_donations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.user_id == current_user.id).first()
    if not donor:
        return []
    donations = db.query(Donation).filter(Donation.donor_id == donor.id).all()
    return donations

@router.get("/eligibility")
def check_eligibility(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.user_id == current_user.id).first()
    if not donor:
        return {"eligible": True, "message": "Eligible"}
    return get_donor_eligibility(donor.last_donation)
