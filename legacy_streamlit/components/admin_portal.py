import streamlit as st
from database import (
    get_all_hospitals, update_hospital_verification, get_all_donors,
    get_all_blood_banks, get_system_stats
)

def render_admin_portal():
    st.markdown("""
        <div class="hero-banner" style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);">
            <h1 class="hero-title">🛡️ LIFELINK ADMIN PORTAL</h1>
            <p class="hero-subtitle">Platform Governance, Hospital Licensing Verification & Operational Controls</p>
        </div>
    """, unsafe_allow_html=True)

    stats = get_system_stats()

    # System Overview KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Donors</div>
                <div class="metric-value">{stats['total_donors']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Verified Hospitals</div>
                <div class="metric-value" style="color: #16A34A;">{stats['verified_hospitals']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Pending Hospital Verifications</div>
                <div class="metric-value" style="color: #EA580C;">{stats['pending_hospitals']}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Blood Units</div>
                <div class="metric-value" style="color: #DC2626;">{stats['total_blood_units']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    tab_hospitals, tab_donors, tab_bbs = st.tabs(["🏥 Hospital Verifications", "👤 Registered Donors", "🩸 Blood Banks Directory"])

    with tab_hospitals:
        st.subheader("🏥 Hospital Verification & Licensing")
        hospitals = get_all_hospitals()

        pending_hospitals = [h for h in hospitals if h["verification_status"] == "PENDING"]
        verified_hospitals = [h for h in hospitals if h["verification_status"] == "VERIFIED"]

        if pending_hospitals:
            st.markdown("### ⏳ Pending Verification Requests")
            for h in pending_hospitals:
                with st.expander(f"🏥 {h['hospital_name']} (License: {h['license_number']})", expanded=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.write(f"**Type:** {h['hospital_type']}")
                        st.write(f"**City:** {h['city']} | **Address:** {h['address']}")
                        st.write(f"**Contact Person:** {h['contact_person']} ({h['phone']})")
                        st.write(f"**Emergency Contact:** {h['emergency_contact']}")
                    with c2:
                        if st.button("✅ Approve Hospital", key=f"app_h_{h['hospital_id']}", type="primary", use_container_width=True):
                            update_hospital_verification(h['hospital_id'], "VERIFIED")
                            st.success(f"{h['hospital_name']} verified successfully!")
                            st.rerun()

                        if st.button("❌ Reject", key=f"rej_h_{h['hospital_id']}", use_container_width=True):
                            update_hospital_verification(h['hospital_id'], "REJECTED")
                            st.warning(f"{h['hospital_name']} rejected.")
                            st.rerun()

        st.markdown("### ✅ Verified Hospitals Network")
        st.dataframe(verified_hospitals, use_container_width=True)

    with tab_donors:
        st.subheader("👤 Registered Donors Directory")
        donors = get_all_donors()
        st.dataframe(donors, use_container_width=True)

    with tab_bbs:
        st.subheader("🩸 Registered Blood Banks Directory")
        bbs = get_all_blood_banks()
        st.dataframe(bbs, use_container_width=True)
