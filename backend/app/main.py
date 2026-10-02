from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import engine, Base
from backend.app.seed import seed_backend_db
from backend.app.routers import (
    auth, emergency_board, donor, hospital,
    blood_bank, admin, matching, analytics, notifications
)

# Initialize Database Schema & Seed Data
Base.metadata.create_all(bind=engine)
seed_backend_db()

app = FastAPI(
    title="LifeLink API - Emergency Blood Management Platform",
    description="Backend API supporting Donors, Hospitals, Blood Banks, and Admin workflows.",
    version="2.0.0"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router)
app.include_router(emergency_board.router)
app.include_router(donor.router)
app.include_router(hospital.router)
app.include_router(blood_bank.router)
app.include_router(admin.router)
app.include_router(matching.router)
app.include_router(analytics.router)
app.include_router(notifications.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "LifeLink Emergency Blood Management System API",
        "docs_url": "/docs",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
