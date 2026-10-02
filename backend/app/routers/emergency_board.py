from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.database import get_db
from backend.app.models.all_models import BloodRequest, Hospital
from backend.app.schemas.schemas import BloodRequestOut

router = APIRouter(prefix="/api/emergency-board", tags=["Emergency Board"])

@router.get("/", response_model=List[BloodRequestOut])
def get_emergency_board(priority: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(BloodRequest).join(Hospital).filter(BloodRequest.status == "ACTIVE")

    if priority and priority.upper() != "ALL":
        query = query.filter(BloodRequest.priority == priority.upper())

    requests = query.order_by(BloodRequest.created_at.desc()).all()

    result = []
    for r in requests:
        resp_count = len(r.responses) if r.responses else 0
        r_dict = {
            "id": r.id,
            "hospital_id": r.hospital_id,
            "hospital_name": r.hospital.hospital_name if r.hospital else "Hospital",
            "patient_reference": r.patient_reference,
            "blood_group": r.blood_group,
            "units_required": r.units_required,
            "priority": r.priority,
            "required_date": r.required_date,
            "location": r.location,
            "contact_dept": r.contact_dept,
            "created_at": r.created_at,
            "status": r.status,
            "response_count": resp_count
        }
        result.append(r_dict)

    return result
