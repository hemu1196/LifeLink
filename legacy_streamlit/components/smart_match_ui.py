import streamlit as st
from matching import find_matched_donors_for_request, calculate_donor_match_score, check_blood_bank_stock_for_request
from database import get_all_donors
from utils.helpers import COMPATIBILITY_RECIPIENT_TO_DONORS

def render_smart_match_tool():
    st.markdown("""
        <div class="hero-banner" style="background: linear-gradient(135deg, #4338CA 0%, #312E81 100%);">
            <h1 class="hero-title">🧠 SMART MATCHING ENGINE</h1>
            <p class="hero-subtitle">Explainable rule-based algorithm evaluating blood compatibility, eligibility, location proximity & availability.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        target_bg = st.selectbox("Select Target Blood Group Needed:", ["O-", "O+", "A+", "A-", "B+", "B-", "AB+", "AB-"])
    with c2:
        target_city = st.text_input("Target City / Location:", value="Coimbatore")
    with c3:
        target_area = st.text_input("Target Area / Locality:", value="Peelamedu")

    st.markdown("---")

    # 1. Compatibility Matrix View
    st.subheader("🩸 1. Blood Group Compatibility Rules")
    compatible_donors = COMPATIBILITY_RECIPIENT_TO_DONORS.get(target_bg, [])
    st.info(f"For recipient with **{target_bg}** blood group, compatible donor blood groups are: **{', '.join(compatible_donors)}**")

    # 2. Blood Bank Stock Check
    bb_stock = check_blood_bank_stock_for_request(target_bg)
    col_bb1, col_bb2 = st.columns(2)
    with col_bb1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Exact Blood Bank Inventory ({target_bg})</div>
                <div class="metric-value">{bb_stock['exact_units']} Units</div>
            </div>
        """, unsafe_allow_html=True)
    with col_bb2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Compatible Blood Bank Inventory</div>
                <div class="metric-value" style="color: #2563EB;">{bb_stock['compatible_units']} Units</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🎯 2. Ranked Suitable Donors (Smart Algorithmic Match)")

    all_donors = get_all_donors()
    mock_request = {
        "blood_group": target_bg,
        "location": f"{target_area}, {target_city}",
        "hospital_city": target_city
    }

    matched_list = []
    for donor in all_donors:
        match_res = calculate_donor_match_score(donor, mock_request)
        if match_res["eligible"]:
            d_entry = dict(donor)
            d_entry["match_score"] = match_res["match_score"]
            d_entry["details"] = match_res
            matched_list.append(d_entry)

    matched_list.sort(key=lambda x: x["match_score"], reverse=True)

    if not matched_list:
        st.warning("No compatible & eligible donors found matching this criteria.")
    else:
        st.markdown(f"Found **{len(matched_list)}** matching donor(s):")

        for idx, d in enumerate(matched_list, 1):
            dt = d["details"]
            score = d["match_score"]
            score_class = "match-high" if score >= 80 else "match-medium"

            with st.container():
                st.markdown(f"""
                    <div style="background: white; border: 1px solid #E2E8F0; padding: 16px; border-radius: 12px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0;">{idx}. 👤 {d['name']} (<span style="color: #DC2626;">🩸 {d['blood_group']}</span>)</h4>
                            <span class="{score_class}" style="font-size: 1.1rem;">🎯 {score}% Match</span>
                        </div>
                        <p style="color: #475569; margin-top: 6px; margin-bottom: 4px;">
                            📍 Location: <strong>{d['area']}, {d['city']}</strong> | 📞 Phone: {d['phone']} | 📅 Last Donation: {d.get('last_donation') or 'Never'}
                        </p>
                        <div style="margin-top: 6px;">
                            <span class="pill pill-normal">✓ {dt['bg_desc']}</span>
                            <span class="pill pill-verified">✓ {dt['loc_desc']}</span>
                            <span class="pill pill-normal">✓ {dt['eligibility_desc']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
