# 🩸 LIFELINK
### Smart Blood Donor, Hospital & Emergency Blood Management System (v2.0 Full-Stack Architecture)

**LifeLink** is a centralized emergency blood coordination platform connecting verified hospitals, blood banks, and eligible donors.

---

## 📁 Repository Structure

```
LifeLink/
│
├── frontend/                     # React (Vite) Single Page Application
│   ├── src/
│   │   ├── components/           # Navbar, Sidebar, EmergencyCard, LoadingSpinner
│   │   ├── pages/
│   │   │   ├── Donor/            # Donor Dashboard, Profile, Eligibility, Responses, History
│   │   │   ├── Hospital/         # Hospital Dashboard, Create Request, Manage Requests, Responses
│   │   │   ├── BloodBank/        # Stock Overview, Add Stock, Batch Inventory
│   │   │   └── Admin/            # Admin Overview, Hospital Verifications
│   │   ├── services/
│   │   │   └── api.js            # Axios API client with automatic JWT bearer injection
│   │   ├── context/
│   │   │   └── AuthContext.jsx   # Auth provider managing token & user session state
│   │   ├── App.jsx               # React Router DOM layout & page definitions
│   │   └── main.jsx
│   ├── package.json
│   └── .env
│
├── backend/                      # FastAPI Python REST Backend API
│   ├── app/
│   │   ├── main.py               # Application entry point with CORS & router setup
│   │   ├── database.py           # SQLAlchemy database configuration & session factory
│   │   ├── models/               # SQLAlchemy ORM models (User, Donor, Hospital, BloodBank, etc.)
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── routers/              # API Endpoints (Auth, Board, Donor, Hospital, BloodBank, Admin, etc.)
│   │   ├── services/
│   │   │   ├── matching.py       # Smart Matching engine
│   │   │   ├── compatibility.py  # Blood Group compatibility matrix
│   │   │   └── eligibility.py    # Donor eligibility calculator
│   │   ├── security/             # JWT token handling & password hashing
│   │   └── seed.py               # Database initial seed script
│   ├── alembic/                  # Database migration configuration
│   ├── requirements.txt
│   └── .env
│
└── legacy_streamlit/             # Monolithic Python Streamlit Prototype
    ├── app.py
    ├── database.py
    ├── matching.py
    ├── seed_data.py
    ├── components/
    └── utils/
```

---

## 🚀 How to Run the Application

### 1. Launch FastAPI Backend
```bash
cd /Users/hemachandra/LifeLink/backend
python3 -m uvicorn backend.app.main:app --reload --port 8000
```
- Interactive API Swagger Documentation: `http://localhost:8000/docs`

### 2. Launch React Frontend
```bash
cd /Users/hemachandra/LifeLink/frontend
npm run dev
```
- Web Application UI: `http://localhost:3000`

### 3. Launch Legacy Streamlit Version (Optional)
```bash
cd /Users/hemachandra/LifeLink/legacy_streamlit
streamlit run app.py
```

---

## 🔑 Quick Demo Login Credentials

| Role | Email | Password | Account Details |
| :--- | :--- | :--- | :--- |
| **👤 Donor** | `rahul@gmail.com` | `donor123` | Rahul Verma (`O-` Donor, Eligible) |
| **🏥 Hospital** | `cityhospital@gmail.com` | `hospital123` | City Hospital (Verified) |
| **🩸 Blood Bank** | `cbebloodbank@gmail.com` | `bloodbank123` | Central Blood Bank |
| **🛡️ Admin** | `admin@lifelink.com` | `admin123` | System Administrator |

*(Note: One-click demo login buttons are provided on the React sign-in page for instant role switching!)*
