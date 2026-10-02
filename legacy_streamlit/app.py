import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="LifeLink - Smart Blood Donor & Emergency Management System",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.styles import load_custom_css
from database import init_db
from seed_data import seed_database
from components.auth import render_auth_page
from components.emergency_board import render_emergency_board
from components.donor_portal import render_donor_portal
from components.hospital_portal import render_hospital_portal
from components.blood_bank_portal import render_blood_bank_portal
from components.admin_portal import render_admin_portal
from components.smart_match_ui import render_smart_match_tool
from components.analytics_ui import render_analytics_dashboard
from components.notifications_ui import render_notifications_ui

# Ensure database is initialized & seeded on first run
init_db()
seed_database()

# Load Custom CSS
load_custom_css()

# Session State Initialization
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "profile" not in st.session_state:
    st.session_state["profile"] = None

# Sidebar Logo & Header
st.sidebar.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🩸 LIFELINK</div>
        <div class="sidebar-subtitle">Smart Blood Emergency Network</div>
    </div>
""", unsafe_allow_html=True)

# User Session Status Bar in Sidebar
if st.session_state.get("user_id"):
    user_role = st.session_state.get("role", "").upper()
    profile_name = "User"
    if st.session_state.get("profile"):
        profile = st.session_state["profile"]
        profile_name = profile.get("name") or profile.get("hospital_name") or profile.get("name") or "User"

    st.sidebar.markdown(f"""
        <div style="background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 8px; padding: 10px; margin-bottom: 15px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #64748B;">LOGGED IN AS</div>
            <div style="font-size: 1rem; font-weight: 700; color: #0F172A;">{profile_name}</div>
            <span class="pill pill-verified" style="margin-top: 4px;">{user_role}</span>
        </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Log Out", use_container_width=True):
        st.session_state["user_id"] = None
        st.session_state["role"] = None
        st.session_state["profile"] = None
        st.rerun()

st.sidebar.markdown("---")

# Main Navigation Menu
nav_options = [
    "🚨 Live Emergency Board",
    "👤 Donor Portal",
    "🏥 Hospital Portal",
    "🩸 Blood Bank Portal",
    "🧠 Smart Match Engine",
    "📊 Analytics & Insights",
    "🔔 Notifications",
    "🛡️ Admin Portal",
    "🔐 Account Sign In / Register"
]

default_index = 0
if not st.session_state.get("user_id"):
    default_index = 0

choice = st.sidebar.radio("📌 Navigation Menu", nav_options, index=default_index)

st.sidebar.markdown("---")
st.sidebar.caption("🩸 **LifeLink v2.0** • Emergency Blood Management")

# Routing Logic
if choice == "🚨 Live Emergency Board":
    render_emergency_board()

elif choice == "👤 Donor Portal":
    if not st.session_state.get("user_id"):
        st.info("Please sign in to access your Donor Portal.")
        render_auth_page()
    elif st.session_state.get("role") != "donor":
        st.warning(f"You are currently logged in as **{st.session_state.get('role').upper()}**. Please log out to access Donor Portal.")
    else:
        render_donor_portal()

elif choice == "🏥 Hospital Portal":
    if not st.session_state.get("user_id"):
        st.info("Please sign in to access Hospital Portal.")
        render_auth_page()
    elif st.session_state.get("role") != "hospital":
        st.warning(f"You are currently logged in as **{st.session_state.get('role').upper()}**. Please log out to access Hospital Portal.")
    else:
        render_hospital_portal()

elif choice == "🩸 Blood Bank Portal":
    if not st.session_state.get("user_id"):
        st.info("Please sign in to access Blood Bank Portal.")
        render_auth_page()
    elif st.session_state.get("role") != "blood_bank":
        st.warning(f"You are currently logged in as **{st.session_state.get('role').upper()}**. Please log out to access Blood Bank Portal.")
    else:
        render_blood_bank_portal()

elif choice == "🧠 Smart Match Engine":
    render_smart_match_tool()

elif choice == "📊 Analytics & Insights":
    render_analytics_dashboard()

elif choice == "🔔 Notifications":
    render_notifications_ui()

elif choice == "🛡️ Admin Portal":
    if not st.session_state.get("user_id"):
        st.info("Please sign in as Administrator.")
        render_auth_page()
    elif st.session_state.get("role") != "admin":
        st.warning("Admin Portal is restricted to platform administrators.")
    else:
        render_admin_portal()

elif choice == "🔐 Account Sign In / Register":
    render_auth_page()
