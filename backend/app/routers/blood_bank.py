from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from backend.app.database import get_db
from backend.app.models.all_models import User, BloodBank, BloodInventory
from backend.app.schemas.schemas import BloodInventoryCreate, BloodInventoryOut
from backend.app.security.auth import get_current_user

router = APIRouter(prefix="/api/blood-bank", tags=["Blood Bank Portal"])

@router.get("/summary")
def get_inventory_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bb = db.query(BloodBank).filter(BloodBank.user_id == current_user.id).first()
    if not bb:
        raise HTTPException(status_code=404, detail="Blood bank profile not found.")

    summary = db.query(
        BloodInventory.blood_group,
        func.sum(BloodInventory.units).label("total_units")
    ).filter(
        BloodInventory.blood_bank_id == bb.id,
        BloodInventory.status == "AVAILABLE"
    ).group_by(BloodInventory.blood_group).all()

    return [{"blood_group": s.blood_group, "total_units": s.total_units} for s in summary]

@router.get("/inventory", response_model=List[BloodInventoryOut])
def get_inventory_items(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bb = db.query(BloodBank).filter(BloodBank.user_id == current_user.id).first()
    if not bb:
        return []

    items = db.query(BloodInventory).filter(BloodInventory.blood_bank_id == bb.id).order_by(BloodInventory.expiry_date.asc()).all()
    out = []
    for item in items:
        out.append({
            "id": item.id,
            "blood_bank_id": item.blood_bank_id,
            "blood_bank_name": bb.name,
            "blood_group": item.blood_group,
            "units": item.units,
            "collection_date": item.collection_date,
            "expiry_date": item.expiry_date,
            "status": item.status
        })
    return out

@router.post("/add", response_model=BloodInventoryOut)
def add_inventory(payload: BloodInventoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bb = db.query(BloodBank).filter(BloodBank.user_id == current_user.id).first()
    if not bb:
        raise HTTPException(status_code=404, detail="Blood bank profile not found.")

    item = BloodInventory(
        blood_bank_id=bb.id,
        blood_group=payload.blood_group,
        units=payload.units,
        collection_date=payload.collection_date,
        expiry_date=payload.expiry_date,
        status="AVAILABLE"
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "blood_bank_id": item.blood_bank_id,
        "blood_bank_name": bb.name,
        "blood_group": item.blood_group,
        "units": item.units,
        "collection_date": item.collection_date,
        "expiry_date": item.expiry_date,
        "status": item.status
    }
