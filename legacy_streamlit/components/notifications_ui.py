import streamlit as st
from database import get_user_notifications, mark_notification_as_read

def render_notifications_ui():
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please log in to view in-app notifications.")
        return

    st.markdown("""
        <div class="hero-banner" style="background: linear-gradient(135deg, #059669 0%, #047857 100%);">
            <h1 class="hero-title">🔔 SMART IN-APP NOTIFICATIONS</h1>
            <p class="hero-subtitle">Real-time alerts for emergency blood requests, donor responses & donation updates.</p>
        </div>
    """, unsafe_allow_html=True)

    notifications = get_user_notifications(user_id)

    if not notifications:
        st.info("🎉 You have no notifications right now.")
        return

    st.markdown(f"**Showing {len(notifications)} notification(s):**")

    for notif in notifications:
        is_unread = notif["read_status"] == 0
        bg_color = "#FEF2F2" if is_unread else "white"
        border_color = "#FCA5A5" if is_unread else "#E2E8F0"

        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                    <div style="background: {bg_color}; border: 1px solid {border_color}; padding: 14px; border-radius: 10px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: #0F172A;">{notif['title']}</h4>
                            <small style="color: #64748B;">{notif['created_at']}</small>
                        </div>
                        <p style="color: #334155; margin-top: 6px; margin-bottom: 0;">{notif['message']}</p>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                if is_unread:
                    if st.button("Mark Read", key=f"n_read_{notif['notification_id']}"):
                        mark_notification_as_read(notif['notification_id'])
                        st.rerun()
