from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- AUTH SCHEMAS ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str # donor, hospital, blood_bank
    name: Optional[str] = None
    blood_group: Optional[str] = None
    age: Optional[int] = 25
    gender: Optional[str] = "Male"
    phone: Optional[str] = None
    city: Optional[str] = "Coimbatore"
    area: Optional[str] = "Peelamedu"
    license_number: Optional[str] = None
    hospital_type: Optional[str] = "Multispecialty"
    address: Optional[str] = None
    contact_person: Optional[str] = None
    emergency_contact: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    email: str
    profile: Optional[dict] = None

# --- DONOR SCHEMAS ---
class DonorUpdate(BaseModel):
    name: str
    phone: str
    city: str
    area: Optional[str] = ""
    last_donation: Optional[str] = ""
    availability: Optional[str] = "AVAILABLE"

class DonorOut(BaseModel):
    id: int
    user_id: int
    name: str
    blood_group: str
    age: Optional[int]
    gender: Optional[str]
    phone: str
    city: str
    area: Optional[str]
    last_donation: Optional[str]
    availability: str

    class Config:
        from_attributes = True

# --- HOSPITAL SCHEMAS ---
class HospitalOut(BaseModel):
    id: int
    user_id: int
    hospital_name: str
    license_number: str
    hospital_type: Optional[str]
    address: Optional[str]
    city: str
    contact_person: Optional[str]
    phone: str
    emergency_contact: Optional[str]
    verification_status: str

    class Config:
        from_attributes = True

# --- BLOOD BANK SCHEMAS ---
class BloodBankOut(BaseModel):
    id: int
    user_id: int
    name: str
    license_number: Optional[str]
    address: Optional[str]
    city: str
    contact_person: Optional[str]
    phone: str
    verification_status: str

    class Config:
        from_attributes = True

# --- BLOOD REQUEST SCHEMAS ---
class BloodRequestCreate(BaseModel):
    patient_reference: str
    blood_group: str
    units_required: int
    priority: str # CRITICAL, URGENT, NORMAL
    required_date: str
    location: str
    contact_dept: str

class BloodRequestOut(BaseModel):
    id: int
    hospital_id: int
    hospital_name: Optional[str] = None
    patient_reference: str
    blood_group: str
    units_required: int
    priority: str
    required_date: str
    location: str
    contact_dept: Optional[str]
    created_at: Optional[datetime]
    status: str
    response_count: Optional[int] = 0

    class Config:
        from_attributes = True

# --- DONOR RESPONSE SCHEMAS ---
class ResponseStatusUpdate(BaseModel):
    status: str # ACCEPTED, CONTACTED, DECLINED, COMPLETED

class DonorResponseOut(BaseModel):
    id: int
    request_id: int
    donor_id: int
    donor_name: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    response_date: Optional[datetime]
    status: str
    patient_reference: Optional[str] = None
    hospital_name: Optional[str] = None
    required_date: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True

# --- BLOOD INVENTORY SCHEMAS ---
class BloodInventoryCreate(BaseModel):
    blood_group: str
    units: int
    collection_date: str
    expiry_date: str

class BloodInventoryOut(BaseModel):
    id: int
    blood_bank_id: int
    blood_bank_name: Optional[str] = None
    blood_group: str
    units: int
    collection_date: str
    expiry_date: str
    status: str

    class Config:
        from_attributes = True

# --- NOTIFICATION SCHEMAS ---
class NotificationOut(BaseModel):
    id: int
    user_id: int
    request_id: Optional[int]
    title: Optional[str]
    message: str
    created_at: Optional[datetime]
    read_status: int

    class Config:
        from_attributes = True
