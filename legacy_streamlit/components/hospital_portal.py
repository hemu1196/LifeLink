import streamlit as st
from datetime import datetime, timedelta
from database import (
    get_hospital_by_user_id, create_blood_request, get_requests_by_hospital,
    get_responses_for_request, update_response_status, update_request_status,
    record_donation, create_notification, get_user_by_id
)
from matching import find_matched_donors_for_request, check_blood_bank_stock_for_request
from utils.helpers import get_priority_color

def render_hospital_portal():
    user_id = st.session_state.get("user_id")
    hospital = get_hospital_by_user_id(user_id)

    if not hospital:
        st.error("Hospital profile not found.")
        return

    # Check Verification Status
    is_verified = hospital["verification_status"] == "VERIFIED"

    # Sidebar Navigation
    menu = st.sidebar.radio(
        "🏥 Hospital Navigation",
        ["🏠 Dashboard", "➕ Create Blood Request", "🚨 Active Emergency Requests", "👥 Donor Responses", "📜 Request History"],
        key="hospital_nav"
    )

    if not is_verified:
        st.warning(f"⚠️ Hospital Verification Status: **{hospital['verification_status']}**. Publishing live emergency requests is restricted until Admin verifies your registration license (`{hospital['license_number']}`).")

    # Fetch hospital's requests
    h_requests = get_requests_by_hospital(hospital["hospital_id"])
    active_reqs = [r for r in h_requests if r["status"] == "ACTIVE"]
    critical_reqs = [r for r in active_reqs if r["priority"] == "CRITICAL"]
    fulfilled_reqs = [r for r in h_requests if r["status"] == "FULFILLED"]
    
    total_responses = sum(r.get("response_count", 0) for r in h_requests)

    if menu == "🏠 Dashboard":
        st.markdown(f"## 🏥 **{hospital['hospital_name']}** Dashboard")
        st.markdown(f"📍 **City:** {hospital['city']} | 📄 **License:** `{hospital['license_number']}` | Status: **{hospital['verification_status']}**")
        st.markdown("---")

        # KPI Metric Cards matching mockup
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Active Requests</div>
                    <div class="metric-value">{len(active_reqs)}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid #DC2626;">
                    <div class="metric-title">Critical Requests</div>
                    <div class="metric-value" style="color: #DC2626;">{len(critical_reqs)}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Donors Responded</div>
                    <div class="metric-value" style="color: #2563EB;">{total_responses}</div>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Requests Fulfilled</div>
                    <div class="metric-value" style="color: #16A34A;">{len(fulfilled_reqs)}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🚨 Quick View: Active Emergency Requirements")

        if not active_reqs:
            st.info("No active emergency blood requests. Click '+ Create Blood Request' to publish a requirement.")
        else:
            for req in active_reqs[:3]:
                st.markdown(f"""
                    <div class="emergency-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin:0;">Ref: <code>{req['patient_reference']}</code> | Blood Required: <span style="color:#DC2626; font-size:1.3rem;">{req['blood_group']}</span> ({req['units_required']} Units)</h4>
                            <span class="pill pill-critical">{req['priority']}</span>
                        </div>
                        <p style="color:#64748B; margin-top:5px; margin-bottom:0;">
                            ⏰ Required By: {req['required_date']} | 📥 Responded Donors: <strong>{req.get('response_count', 0)}</strong>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

    elif menu == "➕ Create Blood Request":
        st.subheader("➕ Create Emergency Blood Request")
        st.caption("For patient privacy, use a reference code (e.g., PT1025) instead of public medical details.")

        with st.form("create_request_form"):
            col1, col2 = st.columns(2)
            with col1:
                patient_ref = st.text_input("Patient Reference Code *", value="PT1030")
                blood_group = st.selectbox("Blood Group Required *", ["O-", "O+", "A+", "A-", "B+", "B-", "AB+", "AB-"])
                units_req = st.number_input("Units Required *", min_value=1, max_value=20, value=3)
            with col2:
                priority = st.selectbox("Priority Level *", ["CRITICAL", "URGENT", "NORMAL"])
                req_date = st.date_input("Required By Date", value=datetime.now().date())
                req_time = st.time_input("Required By Time", value=datetime.now().time())
                dept_contact = st.text_input("Contact Department *", value="Emergency Department (+91 98765 43211)")

            submit_req = st.form_submit_button("🚨 Publish Emergency Blood Request", type="primary", disabled=not is_verified)

            if submit_req:
                if not is_verified:
                    st.error("Hospital must be VERIFIED by Admin before publishing requests.")
                else:
                    date_time_str = f"{req_date.strftime('%Y-%m-%d')} {req_time.strftime('%I:%M %p')}"
                    location_str = f"{hospital['address']}, {hospital['city']}"

                    req_id = create_blood_request(
                        hospital_id=hospital["hospital_id"],
                        patient_reference=patient_ref,
                        blood_group=blood_group,
                        units_required=units_req,
                        priority=priority,
                        required_date=date_time_str,
                        location=location_str,
                        contact_dept=dept_contact
                    )
                    st.success(f"🎉 Emergency Request `{patient_ref}` published on Live Emergency Board!")

    elif menu == "🚨 Active Emergency Requests":
        st.subheader("🚨 Active Hospital Blood Requests")

        if not active_reqs:
            st.info("No active requests.")
        else:
            for req in active_reqs:
                with st.expander(f"🔴 Request: {req['patient_reference']} - {req['blood_group']} ({req['units_required']} Units) [{req['priority']}]", expanded=True):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.write(f"**Required Date:** {req['required_date']}")
                        st.write(f"**Location:** {req['location']}")
                        st.write(f"**Department Contact:** {req['contact_dept']}")
                        
                        # Check Blood Bank stock availability
                        bb_info = check_blood_bank_stock_for_request(req["blood_group"])
                        st.info(f"🩸 Network Blood Bank Available Units: **{bb_info['exact_units']} exact**, **{bb_info['compatible_units']} total compatible**.")

                    with c2:
                        st.write(f"**Donors Responded:** {req.get('response_count', 0)}")

                        if st.button("Mark as FULFILLED", key=f"fulfill_{req['request_id']}", use_container_width=True, type="primary"):
                            update_request_status(req['request_id'], "FULFILLED")
                            st.success("Request marked as FULFILLED.")
                            st.rerun()

                        if st.button("Cancel Request", key=f"cancel_{req['request_id']}", use_container_width=True):
                            update_request_status(req['request_id'], "CANCELLED")
                            st.warning("Request cancelled.")
                            st.rerun()

                    # Smart Matched Donors Recommendation List
                    st.markdown("#### 🧠 Smart Matched Eligible Donors")
                    matched_donors = find_matched_donors_for_request(req['request_id'])

                    if not matched_donors:
                        st.caption("No eligible matched donors found in database currently.")
                    else:
                        for m_donor in matched_donors[:4]:
                            m_det = m_donor['match_details']
                            st.markdown(f"""
                                <div style="border: 1px solid #CBD5E1; background: #F8FAFC; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;">
                                    <strong>👤 {m_donor['name']}</strong> (Group: <code>{m_donor['blood_group']}</code>) | 
                                    Location: {m_donor['area']}, {m_donor['city']} | 
                                    <span class="match-high">🎯 {m_donor['match_score']}% Match</span>
                                    <br><small style="color: #64748B;">Criteria: {m_det['bg_desc']} • {m_det['loc_desc']}</small>
                                </div>
                            """, unsafe_allow_html=True)

    elif menu == "👥 Donor Responses":
        st.subheader("👥 Donors Responded to Emergency Requests")

        if not h_requests:
            st.info("No blood requests found.")
        else:
            for req in h_requests:
                responses = get_responses_for_request(req["request_id"])
                if responses:
                    st.markdown(f"### 📋 Request `{req['patient_reference']}` ({req['blood_group']} - {req['units_required']} Units)")
                    
                    for resp in responses:
                        cols = st.columns([1, 1.5, 1, 1.2, 2])
                        with cols[0]:
                            st.write(f"**ID:** D{resp['donor_id']}")
                        with cols[1]:
                            st.write(f"**Name:** {resp['donor_name']}")
                            st.caption(f"📞 {resp['phone']}")
                        with cols[2]:
                            st.write(f"🩸 **{resp['blood_group']}**")
                        with cols[3]:
                            st.markdown(f"**Status:** `{resp['status']}`")
                        with cols[4]:
                            ac_col1, ac_col2, ac_col3 = st.columns(3)
                            with ac_col1:
                                if st.button("Accept", key=f"acc_{resp['response_id']}"):
                                    update_response_status(resp['response_id'], "ACCEPTED")
                                    create_notification(resp['donor_user_id'], "✅ Response Accepted!", f"{hospital['hospital_name']} accepted your donation response for request {req['patient_reference']}.")
                                    st.success("Accepted")
                                    st.rerun()
                            with ac_col2:
                                if st.button("Complete", key=f"comp_{resp['response_id']}"):
                                    update_response_status(resp['response_id'], "COMPLETED")
                                    record_donation(resp['donor_id'], hospital['hospital_id'], req['request_id'])
                                    create_notification(resp['donor_user_id'], "❤️ Donation Completed", f"Thank you for donating blood at {hospital['hospital_name']}!")
                                    st.success("Donation Completed!")
                                    st.rerun()
                            with ac_col3:
                                if st.button("Decline", key=f"dec_{resp['response_id']}"):
                                    update_response_status(resp['response_id'], "DECLINED")
                                    st.warning("Declined")
                                    st.rerun()
                    st.markdown("---")

    elif menu == "📜 Request History":
        st.subheader("📜 Hospital Request History")
        st.dataframe(h_requests, use_container_width=True)
