from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # donor, hospital, blood_bank, admin
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, server_default=func.now())

    donor = relationship("Donor", back_populates="user", uselist=False)
    hospital = relationship("Hospital", back_populates="user", uselist=False)
    blood_bank = relationship("BloodBank", back_populates="user", uselist=False)

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    blood_group = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    phone = Column(String)
    city = Column(String, nullable=False)
    area = Column(String)
    last_donation = Column(String, default="")
    availability = Column(String, default="AVAILABLE")

    user = relationship("User", back_populates="donor")
    responses = relationship("DonorResponse", back_populates="donor")

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    hospital_name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    hospital_type = Column(String)
    address = Column(String)
    city = Column(String, nullable=False)
    contact_person = Column(String)
    phone = Column(String, nullable=False)
    emergency_contact = Column(String)
    verification_status = Column(String, default="PENDING") # PENDING, VERIFIED, REJECTED

    user = relationship("User", back_populates="hospital")
    requests = relationship("BloodRequest", back_populates="hospital")

class BloodBank(Base):
    __tablename__ = "blood_banks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    license_number = Column(String)
    address = Column(String)
    city = Column(String, nullable=False)
    contact_person = Column(String)
    phone = Column(String, nullable=False)
    verification_status = Column(String, default="VERIFIED")

    user = relationship("User", back_populates="blood_bank")
    inventory = relationship("BloodInventory", back_populates="blood_bank")

class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    patient_reference = Column(String, nullable=False)
    blood_group = Column(String, nullable=False)
    units_required = Column(Integer, nullable=False)
    priority = Column(String, nullable=False) # CRITICAL, URGENT, NORMAL
    required_date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact_dept = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String, default="ACTIVE") # ACTIVE, FULFILLED, CANCELLED, EXPIRED

    hospital = relationship("Hospital", back_populates="requests")
    responses = relationship("DonorResponse", back_populates="request")

class DonorResponse(Base):
    __tablename__ = "donor_responses"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("blood_requests.id"), nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=False)
    response_date = Column(DateTime, server_default=func.now())
    status = Column(String, default="INTERESTED") # INTERESTED, ACCEPTED, CONTACTED, DECLINED, COMPLETED

    request = relationship("BloodRequest", back_populates="responses")
    donor = relationship("Donor", back_populates="responses")

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)
    request_id = Column(Integer, ForeignKey("blood_requests.id"), nullable=True)
    donation_date = Column(String, nullable=False)
    units = Column(Integer, default=1)

class BloodInventory(Base):
    __tablename__ = "blood_inventory"

    id = Column(Integer, primary_key=True, index=True)
    blood_bank_id = Column(Integer, ForeignKey("blood_banks.id"), nullable=False)
    donor_id = Column(Integer, nullable=True)
    blood_group = Column(String, nullable=False)
    units = Column(Integer, default=1)
    collection_date = Column(String, nullable=False)
    expiry_date = Column(String, nullable=False)
    status = Column(String, default="AVAILABLE") # AVAILABLE, RESERVED, EXPIRED, USED

    blood_bank = relationship("BloodBank", back_populates="inventory")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_id = Column(Integer, nullable=True)
    title = Column(String)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    read_status = Column(Integer, default=0) # 0 for unread, 1 for read
