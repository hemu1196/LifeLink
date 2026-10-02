from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.database import get_db
from backend.app.models.all_models import Donor, BloodRequest, BloodInventory, Hospital

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    total_donors = db.query(Donor).count()
    available_donors = db.query(Donor).filter(Donor.availability == "AVAILABLE").count()
    total_inventory_units = db.query(func.sum(BloodInventory.units)).filter(BloodInventory.status == "AVAILABLE").scalar() or 0
    active_requests = db.query(BloodRequest).filter(BloodRequest.status == "ACTIVE").count()
    critical_requests = db.query(BloodRequest).filter(BloodRequest.status == "ACTIVE", BloodRequest.priority == "CRITICAL").count()
    fulfilled_requests = db.query(BloodRequest).filter(BloodRequest.status == "FULFILLED").count()

    # Inventory by Blood Group
    inv_by_bg = db.query(
        BloodInventory.blood_group,
        func.sum(BloodInventory.units).label("total_units")
    ).filter(
        BloodInventory.status == "AVAILABLE"
    ).group_by(BloodInventory.blood_group).all()

    inv_list = [{"blood_group": i.blood_group, "total_units": i.total_units} for i in inv_by_bg]

    # Requests by Priority
    req_by_p = db.query(
        BloodRequest.priority,
        func.count(BloodRequest.id).label("count")
    ).group_by(BloodRequest.priority).all()

    p_list = [{"priority": r.priority, "count": r.count} for r in req_by_p]

    return {
        "kpis": {
            "total_donors": total_donors,
            "available_donors": available_donors,
            "total_inventory_units": total_inventory_units,
            "active_requests": active_requests,
            "critical_requests": critical_requests,
            "fulfilled_requests": fulfilled_requests
        },
        "inventory_distribution": inv_list,
        "request_priorities": p_list
    }
