# 🩸 LIFELINK
### Smart Blood Donor, Hospital & Emergency Blood Management System

**LifeLink** is a centralized emergency blood coordination platform connecting verified hospitals, blood banks, and eligible donors. It enables hospitals to publish urgent requirements and quickly identify suitable blood resources in real time.

---

## 🌟 Key Features & Unique Version Capabilities

1. **🚨 Live Emergency Board**: Verified hospitals publish active requirements with priority tags (🔴 Critical, 🟠 Urgent, 🟢 Normal), required dates, and privacy-preserving patient references (`PT1025`).
2. **🏥 Hospital Portal**: Hospitals can manage active emergency requests, view AI/rule-matched donors, track responses (`[Accept]`, `[Contact]`, `[Decline]`), and mark requirements as fulfilled.
3. **❤️ "I Can Donate" Response System**: Donors can click "I Can Donate" directly on emergency requests. The system validates blood compatibility, 90-day donation interval eligibility, and current availability status.
4. **🧠 Explainable Smart Matching Engine**: A rule-based algorithm calculating match percentages based on:
   - **55% Blood Compatibility** (Exact match vs Compatible/Universal donor)
   - **30% Proximity** (Same area, same city)
   - **15% Donor Eligibility** (Days since last donation, active status)
5. **🩸 Blood Bank Inventory Integration**: Blood banks manage unit batches with collection and expiry dates, providing real-time network stock visibility and expiry/low-stock alerts.
6. **📊 Real-Time Analytics & Visualizations**: Interactive Plotly charts displaying blood group stock distribution, emergency request priority breakdown, and monthly donation trends.
7. **🛡️ Admin Governance Portal**: Verification portal for platform administrators to review hospital registration licenses before granting emergency publishing rights.

---

## 🗃️ Database Architecture (SQLite)

LifeLink is powered by 9 relational tables:
- `users`: User authentication credentials & role definitions (`donor`, `hospital`, `blood_bank`, `admin`).
- `donors`: Donor profiles, blood group, last donation date, availability status.
- `hospitals`: Hospital license numbers, registration status (`PENDING`, `VERIFIED`), contact details.
- `blood_banks`: Blood bank registrations, licenses, and location info.
- `blood_requests`: Emergency requirements published by hospitals.
- `donor_responses`: Responses submitted by donors ("I Can Donate").
- `donations`: Logged past donation records.
- `blood_inventory`: Batch blood inventory tracking collection & expiry dates.
- `notifications`: In-app notification store.

---

## 🚀 How to Run the Application

### 1. Navigate to Project Directory
```bash
cd /Users/hemachandra/LifeLink
```

### 2. Launch Streamlit App
```bash
streamlit run app.py
```

The app automatically initializes the SQLite database (`lifelink.db`) and seeds initial sample data on first run.

---

## 🔑 Preset Quick Demo Accounts

For convenient testing during presentation/demo:

| Role | Email | Password | Details |
| :--- | :--- | :--- | :--- |
| **👤 Donor** | `rahul@gmail.com` | `donor123` | Rahul Verma (O- Donor, Eligible) |
| **🏥 Hospital** | `cityhospital@gmail.com` | `hospital123` | City Hospital (Verified Hospital) |
| **🩸 Blood Bank** | `cbebloodbank@gmail.com` | `bloodbank123` | Central Blood Bank |
| **🛡️ Admin** | `admin@lifelink.com` | `admin123` | System Administrator |

*(Note: One-click login buttons are also provided on the sign-in page for instant switching between roles!)*
