import streamlit as st
import plotly.express as px
import pandas as pd
from database import get_system_stats, get_inventory_summary, get_all_active_requests, get_connection

def render_analytics_dashboard():
    st.markdown("""
        <div class="hero-banner" style="background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);">
            <h1 class="hero-title">📊 ANALYTICS & SYSTEM INSIGHTS</h1>
            <p class="hero-subtitle">Real-time telemetry, blood availability trends, emergency response metrics & donation analytics.</p>
        </div>
    """, unsafe_allow_html=True)

    stats = get_system_stats()

    # KPI Summary Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Donors</div>
                <div class="metric-value">{stats['total_donors']}</div>
                <small style="color: #16A34A;">{stats['available_donors']} Available</small>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Available Blood Stock</div>
                <div class="metric-value" style="color: #DC2626;">{stats['total_blood_units']} Units</div>
                <small style="color: #64748B;">Network Inventory</small>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Active Emergency Requests</div>
                <div class="metric-value" style="color: #EA580C;">{stats['active_requests']}</div>
                <small style="color: #DC2626;">{stats['critical_requests']} Critical</small>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Fulfilled Requests</div>
                <div class="metric-value" style="color: #16A34A;">{stats['fulfilled_requests']}</div>
                <small style="color: #16A34A;">Completed Donations</small>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Chart Row 1: Blood Inventory Distribution & Emergency Request Priorities
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("🩸 Blood Group Stock Distribution")
        inv_summary = get_inventory_summary()
        if inv_summary:
            df_inv = pd.DataFrame(inv_summary)
            fig_inv = px.bar(
                df_inv,
                x="blood_group",
                y="total_units",
                color="blood_group",
                labels={"blood_group": "Blood Group", "total_units": "Units Available"},
                color_discrete_sequence=px.colors.qualitative.Bold,
                text_auto=True
            )
            fig_inv.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_inv, use_container_width=True)
        else:
            st.info("No blood stock data available.")

    with col_c2:
        st.subheader("🚨 Active Requests Priority Breakdown")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT priority, COUNT(*) as count FROM blood_requests GROUP BY priority")
        p_rows = cursor.fetchall()
        conn.close()

        if p_rows:
            df_p = pd.DataFrame([dict(r) for r in p_rows])
            fig_p = px.pie(
                df_p,
                values="count",
                names="priority",
                color="priority",
                color_discrete_map={"CRITICAL": "#DC2626", "URGENT": "#EA580C", "NORMAL": "#16A34A"}
            )
            fig_p.update_layout(margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_p, use_container_width=True)
        else:
            st.info("No request priority data available.")

    st.markdown("---")

    # Chart Row 2: Monthly Donation Trends
    st.subheader("📈 Monthly Donation Activity Trends")
    # Sample trend data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
    donations_trend = [12, 18, 15, 24, 30, 28, 35, 42, 38, 45]
    df_trend = pd.DataFrame({"Month": months, "Donations": donations_trend})

    fig_trend = px.line(
        df_trend,
        x="Month",
        y="Donations",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#DC2626"]
    )
    fig_trend.update_traces(line_width=3, marker_size=8)
    fig_trend.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_trend, use_container_width=True)
