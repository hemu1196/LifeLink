import streamlit as st
from utils.helpers import hash_password
from database import (
    get_user_by_email, create_user, create_donor, create_hospital,
    create_blood_bank, get_donor_by_user_id, get_hospital_by_user_id,
    get_blood_bank_by_user_id
)

def render_auth_page():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #DC2626; font-size: 2.8rem; font-weight: 800; margin-bottom: 0;">🩸 LifeLink</h1>
            <p style="color: #64748B; font-size: 1.1rem; font-weight: 500;">
                Smart Blood Donor, Hospital & Emergency Blood Management System
            </p>
        </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["🔐 Sign In", "📝 Register New Account"])

    # --- TAB 1: LOGIN ---
    with tab_login:
        col_main, col_demo = st.columns([1.2, 1])

        with col_main:
            st.subheader("Account Login")
            role_type = st.radio("Select Your Role:", ["👤 Donor", "🏥 Hospital", "🩸 Blood Bank", "🛡️ Admin"], horizontal=True)

            role_map = {
                "👤 Donor": "donor",
                "🏥 Hospital": "hospital",
                "🩸 Blood Bank": "blood_bank",
                "🛡️ Admin": "admin"
            }
            selected_role = role_map[role_type]

            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Log In", use_container_width=True, type="primary")

                if submit_login:
                    if not email or not password:
                        st.error("Please provide both email and password.")
                    else:
                        user = get_user_by_email(email)
                        if not user or user["password_hash"] != hash_password(password):
                            st.error("Invalid email or password.")
                        elif user["role"] != selected_role and user["role"] != "admin":
                            st.warning(f"This email belongs to a '{user['role'].upper()}' account. Please select the correct role tab.")
                        else:
                            st.session_state["user_id"] = user["user_id"]
                            st.session_state["role"] = user["role"]
                            st.session_state["email"] = user["email"]

                            # Load profile data
                            if user["role"] == "donor":
                                donor = get_donor_by_user_id(user["user_id"])
                                st.session_state["profile"] = donor
                            elif user["role"] == "hospital":
                                hospital = get_hospital_by_user_id(user["user_id"])
                                st.session_state["profile"] = hospital
                            elif user["role"] == "blood_bank":
                                bb = get_blood_bank_by_user_id(user["user_id"])
                                st.session_state["profile"] = bb
                            
                            st.success("Login successful!")
                            st.rerun()

        with col_demo:
            st.info("💡 **Quick Demo One-Click Login**")
            st.markdown("Use preset demo accounts to quickly test the application:")

            if st.button("👤 Log in as Donor (Rahul - O-)", use_container_width=True):
                user = get_user_by_email("rahul@gmail.com")
                st.session_state["user_id"] = user["user_id"]
                st.session_state["role"] = "donor"
                st.session_state["email"] = user["email"]
                st.session_state["profile"] = get_donor_by_user_id(user["user_id"])
                st.rerun()

            if st.button("🏥 Log in as Hospital (City Hospital)", use_container_width=True):
                user = get_user_by_email("cityhospital@gmail.com")
                st.session_state["user_id"] = user["user_id"]
                st.session_state["role"] = "hospital"
                st.session_state["email"] = user["email"]
                st.session_state["profile"] = get_hospital_by_user_id(user["user_id"])
                st.rerun()

            if st.button("🩸 Log in as Blood Bank (Coimbatore BB)", use_container_width=True):
                user = get_user_by_email("cbebloodbank@gmail.com")
                st.session_state["user_id"] = user["user_id"]
                st.session_state["role"] = "blood_bank"
                st.session_state["email"] = user["email"]
                st.session_state["profile"] = get_blood_bank_by_user_id(user["user_id"])
                st.rerun()

            if st.button("🛡️ Log in as Administrator", use_container_width=True):
                user = get_user_by_email("admin@lifelink.com")
                st.session_state["user_id"] = user["user_id"]
                st.session_state["role"] = "admin"
                st.session_state["email"] = user["email"]
                st.session_state["profile"] = {"name": "System Administrator"}
                st.rerun()

    # --- TAB 2: REGISTER ---
    with tab_register:
        reg_type = st.selectbox("I am registering as:", ["👤 Donor", "🏥 Hospital", "🩸 Blood Bank"])

        if reg_type == "👤 Donor":
            st.subheader("Donor Registration")
            with st.form("donor_reg_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Full Name *")
                    email = st.text_input("Email Address *")
                    password = st.text_input("Password *", type="password")
                    blood_group = st.selectbox("Blood Group *", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                    age = st.number_input("Age *", min_value=18, max_value=70, value=25)
                with col2:
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                    phone = st.text_input("Phone Number *")
                    city = st.text_input("City *", value="Coimbatore")
                    area = st.text_input("Area / Locality", value="Peelamedu")
                    last_donation = st.date_input("Last Donation Date (if any)", value=None)

                submit_reg = st.form_submit_button("Create Donor Account", type="primary")

                if submit_reg:
                    if not name or not email or not password or not phone:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        pwd_hash = hash_password(password)
                        uid = create_user(email, pwd_hash, "donor")
                        if not uid:
                            st.error("Email address already registered!")
                        else:
                            last_don_str = last_donation.strftime("%Y-%m-%d") if last_donation else ""
                            create_donor(uid, name, blood_group, age, gender, phone, city, area, last_don_str)
                            st.success("Donor Account registered successfully! Please log in now.")

        elif reg_type == "🏥 Hospital":
            st.subheader("Hospital Registration")
            st.info("ℹ️ Hospital accounts will undergo verification before emergency publishing rights are enabled.")
            with st.form("hospital_reg_form"):
                col1, col2 = st.columns(2)
                with col1:
                    h_name = st.text_input("Hospital Name *")
                    license_no = st.text_input("Registration / License Number *")
                    h_type = st.selectbox("Hospital Type", ["Multispecialty", "Super Specialty", "Government Hospital", "General Hospital", "Clinic"])
                    email = st.text_input("Official Email *")
                    password = st.text_input("Password *", type="password")
                with col2:
                    contact_person = st.text_input("Contact Person Name *")
                    phone = st.text_input("Official Phone *")
                    emergency_contact = st.text_input("Emergency Department Contact *")
                    city = st.text_input("City *", value="Coimbatore")
                    address = st.text_area("Hospital Address *")

                submit_h_reg = st.form_submit_button("Register Hospital Portal", type="primary")

                if submit_h_reg:
                    if not h_name or not license_no or not email or not password or not phone:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        pwd_hash = hash_password(password)
                        uid = create_user(email, pwd_hash, "hospital")
                        if not uid:
                            st.error("Email address already registered!")
                        else:
                            create_hospital(uid, h_name, license_no, h_type, address, city, contact_person, phone, emergency_contact, "PENDING")
                            st.success("Hospital Registration submitted! Status: PENDING verification by Admin.")

        elif reg_type == "🩸 Blood Bank":
            st.subheader("Blood Bank Registration")
            with st.form("bb_reg_form"):
                col1, col2 = st.columns(2)
                with col1:
                    bb_name = st.text_input("Blood Bank Name *")
                    license_no = st.text_input("License Number *")
                    email = st.text_input("Official Email *")
                    password = st.text_input("Password *", type="password")
                with col2:
                    contact_person = st.text_input("Contact Person Name *")
                    phone = st.text_input("Official Phone *")
                    city = st.text_input("City *", value="Coimbatore")
                    address = st.text_area("Address *")

                submit_bb_reg = st.form_submit_button("Register Blood Bank", type="primary")

                if submit_bb_reg:
                    if not bb_name or not email or not password or not phone:
                        st.error("Please fill in all required fields marked with *")
                    else:
                        pwd_hash = hash_password(password)
                        uid = create_user(email, pwd_hash, "blood_bank")
                        if not uid:
                            st.error("Email address already registered!")
                        else:
                            create_blood_bank(uid, bb_name, license_no, address, city, contact_person, phone, "VERIFIED")
                            st.success("Blood Bank Account registered successfully! Please log in now.")
