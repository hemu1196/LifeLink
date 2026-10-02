from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from backend.app.database import get_db
from backend.app.models.all_models import Donor, BloodRequest, BloodInventory
from backend.app.services.compatibility import COMPATIBILITY_RECIPIENT_TO_DONORS
from backend.app.services.matching import calculate_donor_match_score

router = APIRouter(prefix="/api/matching", tags=["Smart Matching"])

@router.get("/find-donors")
def find_matched_donors(
    blood_group: str = Query(...),
    city: str = Query("Coimbatore"),
    area: Optional[str] = Query("Peelamedu"),
    request_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    donors = db.query(Donor).all()
    matched_donors = []

    req_location = f"{area or ''}, {city}"
    for d in donors:
        d_dict = {
            "id": d.id,
            "name": d.name,
            "blood_group": d.blood_group,
            "age": d.age,
            "phone": d.phone,
            "city": d.city,
            "area": d.area,
            "last_donation": d.last_donation,
            "availability": d.availability
        }
        res = calculate_donor_match_score(d_dict, blood_group, req_location, city)
        if res["eligible"]:
            d_dict["match_score"] = res["match_score"]
            d_dict["match_details"] = res
            matched_donors.append(d_dict)

    matched_donors.sort(key=lambda x: x["match_score"], reverse=True)
    return {
        "blood_group_required": blood_group,
        "compatible_donor_groups": COMPATIBILITY_RECIPIENT_TO_DONORS.get(blood_group, []),
        "matched_donors": matched_donors
    }

@router.get("/stock-check")
def check_blood_bank_stock(blood_group: str = Query(...), db: Session = Depends(get_db)):
    compatible_groups = COMPATIBILITY_RECIPIENT_TO_DONORS.get(blood_group, [])

    summary = db.query(
        BloodInventory.blood_group,
        func.sum(BloodInventory.units).label("total_units")
    ).filter(
        BloodInventory.status == "AVAILABLE"
    ).group_by(BloodInventory.blood_group).all()

    exact_units = 0
    compatible_units = 0

    for s in summary:
        bg = s.blood_group
        units = s.total_units or 0
        if bg == blood_group:
            exact_units += units
        if bg in compatible_groups:
            compatible_units += units

    return {
        "blood_group": blood_group,
        "exact_units": exact_units,
        "compatible_units": compatible_units,
        "has_stock": compatible_units > 0
    }
