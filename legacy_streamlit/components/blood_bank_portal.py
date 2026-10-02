import streamlit as st
from datetime import datetime, timedelta
from database import (
    get_blood_bank_by_user_id, get_inventory_summary, get_all_inventory_items,
    add_blood_inventory
)

def render_blood_bank_portal():
    user_id = st.session_state.get("user_id")
    bb = get_blood_bank_by_user_id(user_id)

    if not bb:
        st.error("Blood Bank profile not found.")
        return

    # Sidebar Navigation
    menu = st.sidebar.radio(
        "🩸 Blood Bank Navigation",
        ["🏠 Dashboard & Stock", "➕ Add Blood Units", "⚠️ Expiry & Low Stock Alerts"],
        key="bb_nav"
    )

    summary = get_inventory_summary(bb["blood_bank_id"])
    all_items = get_all_inventory_items(bb["blood_bank_id"])
    total_units = sum(item["total_units"] for item in summary)

    if menu == "🏠 Dashboard & Stock":
        st.markdown(f"## 🩸 **{bb['name']}** Inventory Portal")
        st.markdown(f"📍 **Location:** {bb['city']} | 📞 **Phone:** {bb['phone']}")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total Blood Units</div>
                    <div class="metric-value" style="color: #DC2626;">{total_units} Units</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Blood Group Types</div>
                    <div class="metric-value">{len(summary)} Groups</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Verification Status</div>
                    <div class="metric-value" style="color: #16A34A; font-size: 1.4rem;">{bb['verification_status']}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🩸 Current Blood Inventory Stock")

        if not summary:
            st.info("No blood inventory items recorded.")
        else:
            grid_cols = st.columns(4)
            all_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            stock_dict = {item["blood_group"]: item["total_units"] for item in summary}

            for idx, bg in enumerate(all_groups):
                units_cnt = stock_dict.get(bg, 0)
                is_low = units_cnt < 3
                with grid_cols[idx % 4]:
                    border_clr = "#DC2626" if is_low else "#E2E8F0"
                    badge_str = "⚠️ LOW STOCK" if is_low else "NORMAL"
                    badge_color = "#FEF2F2" if is_low else "#F0FDF4"
                    txt_color = "#991B1B" if is_low else "#166534"

                    st.markdown(f"""
                        <div style="border: 2px solid {border_clr}; background: white; padding: 15px; border-radius: 12px; margin-bottom: 15px; text-align: center;">
                            <div style="font-size: 1.8rem; font-weight: 800; color: #DC2626;">{bg}</div>
                            <div style="font-size: 1.4rem; font-weight: 700; color: #0F172A; margin: 4px 0;">{units_cnt} Units</div>
                            <span class="pill" style="background-color: {badge_color}; color: {txt_color};">{badge_str}</span>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Detailed Unit Batches")
        st.dataframe(all_items, use_container_width=True)

    elif menu == "➕ Add Blood Units":
        st.subheader("➕ Add New Blood Inventory Batch")
        with st.form("add_inventory_form"):
            col1, col2 = st.columns(2)
            with col1:
                bg = st.selectbox("Blood Group *", ["O-", "O+", "A+", "A-", "B+", "B-", "AB+", "AB-"])
                units = st.number_input("Units Count *", min_value=1, max_value=100, value=5)
            with col2:
                col_date = st.date_input("Collection Date", value=datetime.now().date())
                exp_date = st.date_input("Expiry Date", value=datetime.now().date() + timedelta(days=35))

            submit_add = st.form_submit_button("Save Blood Batch to Inventory", type="primary")

            if submit_add:
                add_blood_inventory(
                    blood_bank_id=bb["blood_bank_id"],
                    blood_group=bg,
                    units=units,
                    collection_date=col_date.strftime("%Y-%m-%d"),
                    expiry_date=exp_date.strftime("%Y-%m-%d")
                )
                st.success(f"Added {units} unit(s) of {bg} blood to inventory!")

    elif menu == "⚠️ Expiry & Low Stock Alerts":
        st.subheader("⚠️ Blood Inventory Alerts")
        today_str = datetime.now().strftime("%Y-%m-%d")

        st.markdown("### ⏳ Units Expiring Soon (< 7 Days)")
        expiring_items = [i for i in all_items if i.get("expiry_date", "") <= (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")]

        if not expiring_items:
            st.success("No blood units expiring in the next 7 days.")
        else:
            st.dataframe(expiring_items, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔴 Critical Low Stock Warning (< 3 Units)")
        stock_dict = {item["blood_group"]: item["total_units"] for item in summary}
        low_groups = [bg for bg, cnt in stock_dict.items() if cnt < 3]

        if not low_groups:
            st.success("All blood groups have sufficient stock.")
        else:
            for lg in low_groups:
                st.error(f"⚠️ **{lg}** stock is critically low! Current available units: **{stock_dict[lg]}**.")
