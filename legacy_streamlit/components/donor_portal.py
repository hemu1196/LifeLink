import streamlit as st
from datetime import datetime
from database import (
    get_donor_by_user_id, update_donor_profile, get_all_active_requests,
    get_responses_by_donor, get_donations_by_donor
)
from utils.helpers import get_donor_eligibility, is_blood_compatible
from components.emergency_board import render_emergency_board

def render_donor_portal():
    user_id = st.session_state.get("user_id")
    donor = get_donor_by_user_id(user_id)

    if not donor:
        st.error("Donor profile not found.")
        return

    # Sidebar / Menu Navigation for Donor
    menu = st.sidebar.radio(
        "👤 Donor Navigation",
        ["🏠 Dashboard", "🚨 Live Emergency Board", "👤 My Profile", "🩺 Eligibility Check", "❤️ My Responses", "📜 Donation History"],
        key="donor_nav"
    )

    if menu == "🏠 Dashboard":
        st.markdown(f"## Welcome back, **{donor['name']}**! 👋")
        
        # KPI Metric Cards
        eligibility = get_donor_eligibility(donor.get("last_donation"))
        elig_status = "🟢 Eligible" if eligibility["eligible"] else "🔴 Not Eligible Yet"
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Blood Group</div>
                    <div class="metric-value" style="color: #DC2626;">🩸 {donor['blood_group']}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Donation Status</div>
                    <div class="metric-value" style="font-size: 1.2rem; font-weight: 700; margin-top: 10px;">{elig_status}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Last Donation</div>
                    <div class="metric-value" style="font-size: 1.2rem; margin-top: 10px;">{donor.get('last_donation') or 'None Logged'}</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Current Availability</div>
                    <div class="metric-value" style="font-size: 1.2rem; color: #16A34A; margin-top: 10px;">{donor.get('availability', 'AVAILABLE')}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Quick Live Emergency Requests (Matching Donor's City / Compatible Group)
        st.subheader("🚨 Compatible Emergency Requirements Near You")
        all_reqs = get_all_active_requests()
        compatible_reqs = [r for r in all_reqs if is_blood_compatible(donor["blood_group"], r["blood_group"])]

        if not compatible_reqs:
            st.info("No active emergency requests compatible with your blood group right now.")
        else:
            for req in compatible_reqs[:3]:
                st.markdown(f"""
                    <div class="emergency-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0;">🏥 {req['hospital_name']} (Required: <span style="color: #DC2626;">{req['blood_group']}</span> - {req['units_required']} Units)</h4>
                            <span class="pill pill-critical">{req['priority']}</span>
                        </div>
                        <p style="color: #64748B; margin-top: 5px; margin-bottom: 0;">📍 Location: {req['location']} | ⏰ Required By: {req['required_date']}</p>
                    </div>
                """, unsafe_allow_html=True)

    elif menu == "🚨 Live Emergency Board":
        render_emergency_board()

    elif menu == "👤 My Profile":
        st.subheader("👤 Manage Profile & Availability")
        with st.form("edit_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", value=donor["name"])
                phone = st.text_input("Phone Number", value=donor["phone"])
                city = st.text_input("City", value=donor["city"])
                area = st.text_input("Area / Locality", value=donor["area"] or "")
            with col2:
                st.text_input("Blood Group (Immutable)", value=donor["blood_group"], disabled=True)
                
                last_don_val = None
                if donor.get("last_donation"):
                    try:
                        last_don_val = datetime.strptime(donor["last_donation"], "%Y-%m-%d").date()
                    except Exception:
                        last_don_val = None

                last_donation = st.date_input("Last Donation Date", value=last_don_val)
                availability = st.selectbox("Donation Availability Status", ["AVAILABLE", "UNAVAILABLE"], index=0 if donor.get("availability") == "AVAILABLE" else 1)

            submit_update = st.form_submit_button("Update Profile", type="primary")

            if submit_update:
                last_don_str = last_donation.strftime("%Y-%m-%d") if last_donation else ""
                update_donor_profile(donor["donor_id"], name, phone, city, area, last_don_str, availability)
                st.success("Profile updated successfully!")
                # Refresh session state
                st.session_state["profile"] = get_donor_by_user_id(user_id)
                st.rerun()

    elif menu == "🩺 Eligibility Check":
        st.subheader("🩺 Smart Donor Eligibility Calculator")
        st.markdown("Check if you are eligible to donate blood today based on official medical guidelines.")

        with st.form("eligibility_wizard"):
            c1, c2 = st.columns(2)
            with c1:
                age_check = st.number_input("Your Age", min_value=15, max_value=80, value=donor["age"] or 25)
                weight_check = st.number_input("Your Weight (kg)", min_value=30, max_value=150, value=65)
                days_since_sick = st.checkbox("I have NOT had a fever/cold/flu in the past 14 days", value=True)
            with c2:
                tattoo_check = st.checkbox("I have NOT had tattoos or major surgery in the past 6 months", value=True)
                meds_check = st.checkbox("I am NOT taking major antibiotics or blood thinners", value=True)

            check_btn = st.form_submit_button("Check Eligibility Status", type="primary")

            if check_btn or True:
                last_don = donor.get("last_donation")
                elig = get_donor_eligibility(last_don)

                reasons = []
                if age_check < 18 or age_check > 65:
                    reasons.append("Age must be between 18 and 65 years.")
                if weight_check < 50:
                    reasons.append("Weight must be at least 50 kg.")
                if not days_since_sick:
                    reasons.append("Must be free from illness for 14 days.")
                if not tattoo_check:
                    reasons.append("Must wait 6 months after tattoo/surgery.")
                if not meds_check:
                    reasons.append("Must not be on antibiotics or blood thinners.")
                if not elig["eligible"]:
                    reasons.append(elig["message"])

                if not reasons:
                    st.success("""
                        ### 🎉 Congratulations! You are FULLY ELIGIBLE to Donate Blood!
                        Your blood group **{}** is ready to save lives. You can respond to emergency blood requests.
                    """.format(donor["blood_group"]))
                else:
                    st.error("### ⚠️ Temporarily Ineligible to Donate")
                    for r in reasons:
                        st.markdown(f"- ❌ {r}")

    elif menu == "❤️ My Responses":
        st.subheader("❤️ My Emergency Donation Responses")
        responses = get_responses_by_donor(donor["donor_id"])

        if not responses:
            st.info("You haven't responded to any emergency requests yet.")
        else:
            for resp in responses:
                status_color = "#16A34A" if resp["status"] in ["ACCEPTED", "COMPLETED"] else "#EA580C"
                st.markdown(f"""
                    <div style="border: 1px solid #E2E8F0; padding: 15px; border-radius: 10px; margin-bottom: 12px; background: white;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0;">🏥 {resp['hospital_name']} (Ref: `{resp['patient_reference']}`)</h4>
                            <span style="font-weight: 700; color: {status_color}; background: #F1F5F9; padding: 4px 10px; border-radius: 6px;">{resp['status']}</span>
                        </div>
                        <p style="color: #64748B; margin-top: 6px; margin-bottom: 0;">
                            🩸 Required: <strong>{resp['req_blood_group']}</strong> | 📍 Location: {resp['location']} | ⏰ Required By: {resp['required_date']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    elif menu == "📜 Donation History":
        st.subheader("📜 Donation History & Impact")
        donations = get_donations_by_donor(donor["donor_id"])

        if not donations:
            st.info("No past donation records logged.")
        else:
            st.dataframe(donations, use_container_width=True)
