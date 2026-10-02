import streamlit as st
from database import (
    get_all_active_requests, submit_donor_response, create_notification,
    get_hospital_by_user_id
)
from utils.helpers import is_blood_compatible, get_donor_eligibility, get_priority_color
from matching import check_blood_bank_stock_for_request

def render_emergency_board():
    st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">🚨 LIVE EMERGENCY BLOOD BOARD</h1>
            <p class="hero-subtitle">Real-time emergency blood requirements published directly by verified hospitals.</p>
        </div>
    """, unsafe_allow_html=True)

    filter_priority = st.radio(
        "Filter by Priority:",
        ["All", "🔴 Critical", "🟠 Urgent", "🟢 Normal"],
        horizontal=True
    )

    priority_map = {
        "All": "ALL",
        "🔴 Critical": "CRITICAL",
        "🟠 Urgent": "URGENT",
        "🟢 Normal": "NORMAL"
    }

    selected_priority = priority_map[filter_priority]
    active_requests = get_all_active_requests(selected_priority)

    if not active_requests:
        st.info("✨ No active emergency blood requirements at the moment.")
        return

    st.markdown(f"**Showing {len(active_requests)} Active Emergency Requirement(s)**")

    for req in active_requests:
        p_color = get_priority_color(req["priority"])
        
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2.2, 1.8, 1.2])

            with col1:
                st.markdown(f"""
                    <div style="text-align: center; background-color: #FEF2F2; padding: 12px; border-radius: 12px; border: 1px solid #FCA5A5;">
                        <span style="font-size: 0.8rem; font-weight: 700; color: #991B1B;">REQUIRED</span>
                        <div style="font-size: 2.2rem; font-weight: 800; color: #DC2626; margin-top: -5px;">{req['blood_group']}</div>
                        <span style="font-size: 0.85rem; font-weight: 600; color: #475569;">💉 {req['units_required']} Unit(s)</span>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"### 🏥 {req['hospital_name']}")
                st.markdown(f"📍 **Location:** {req['location']}")
                st.markdown(f"🏷️ **Ref Code:** `{req['patient_reference']}`")
                st.markdown(f"⏰ **Required By:** `{req['required_date']}`")

            with col3:
                st.markdown(f"""
                    <div style="margin-top: 5px;">
                        <span class="pill" style="background-color: {p_color}22; color: {p_color}; border: 1px solid {p_color};">
                            ● {req['priority']} PRIORITY
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                st.write(f"📞 **Contact Dept:** {req['contact_dept']}")
                
                # Check Blood Bank Stock availability
                bb_stock = check_blood_bank_stock_for_request(req['blood_group'])
                if bb_stock["exact_units"] > 0:
                    st.caption(f"🩸 Blood Bank Stock: **{bb_stock['exact_units']} units** available in network")
                elif bb_stock["compatible_units"] > 0:
                    st.caption(f"🩸 Blood Bank Stock: **{bb_stock['compatible_units']} compatible units** available")
                else:
                    st.caption("🩸 Blood Bank Stock: Low/Unavailable (Donor response needed)")

            with col4:
                st.write("")
                st.write("")
                # Response Button Flow
                donor_profile = st.session_state.get("profile") if st.session_state.get("role") == "donor" else None

                if st.button("❤️ I Can Donate", key=f"donate_btn_{req['request_id']}", use_container_width=True, type="primary"):
                    if not st.session_state.get("user_id"):
                        st.warning("Please sign in as a **Donor** to respond to emergency requests.")
                    elif st.session_state.get("role") != "donor":
                        st.warning("Only registered **Donors** can respond to blood requests.")
                    else:
                        # Validate Donor Compatibility & Eligibility
                        donor_bg = donor_profile["blood_group"]
                        req_bg = req["blood_group"]

                        if not is_blood_compatible(donor_bg, req_bg):
                            st.error(f"⚠️ Blood group incompatible. Your group is **{donor_bg}**, but the request requires **{req_bg}**.")
                        else:
                            elig = get_donor_eligibility(donor_profile.get("last_donation"))
                            if not elig["eligible"]:
                                st.error(f"⚠️ {elig['message']}")
                            else:
                                success = submit_donor_response(req["request_id"], donor_profile["donor_id"])
                                if success:
                                    # Create notification for hospital
                                    h_user = req.get("hospital_id")
                                    create_notification(
                                        user_id=req["hospital_id"],
                                        title="❤️ New Donor Response",
                                        message=f"Donor {donor_profile['name']} ({donor_bg}) responded 'I Can Donate' to request {req['patient_reference']}.",
                                        request_id=req["request_id"]
                                    )
                                    st.success(f"""
                                        🎉 **Response Submitted Successfully!**
                                        
                                        Thank you, {donor_profile['name']}! **{req['hospital_name']}** has received your response for Request `{req['patient_reference']}`.
                                        The hospital team will contact you shortly.
                                    """)
                                else:
                                    st.info("You have already responded to this emergency request!")

        st.markdown("<hr style='margin: 15px 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
