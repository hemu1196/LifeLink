import streamlit as st

def load_custom_css():
    """Inject custom CSS styling into Streamlit app."""
    st.markdown("""
        <style>
        /* Global Styles & Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Sidebar Header Styling */
        .sidebar-header {
            text-align: center;
            padding: 10px 0 20px 0;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        
        .sidebar-logo {
            font-size: 2.2rem;
            font-weight: 800;
            color: #DC2626;
            margin-bottom: 0px;
            letter-spacing: -0.5px;
        }

        .sidebar-subtitle {
            font-size: 0.85rem;
            color: #64748B;
            font-weight: 500;
        }

        /* Custom Cards */
        .metric-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            text-align: left;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .metric-card:hover {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .metric-title {
            font-size: 0.875rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #0F172A;
            margin-top: 4px;
        }

        /* Emergency Cards */
        .emergency-card {
            background-color: #FFFFFF;
            border-left: 5px solid #DC2626;
            border-top: 1px solid #E2E8F0;
            border-right: 1px solid #E2E8F0;
            border-bottom: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }

        .emergency-card-critical {
            border-left-color: #DC2626;
            background-color: #FEF2F2;
        }

        .emergency-card-urgent {
            border-left-color: #EA580C;
            background-color: #FFF7ED;
        }

        .emergency-card-normal {
            border-left-color: #16A34A;
            background-color: #F0FDF4;
        }

        /* Status Pills */
        .pill {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .pill-critical {
            background-color: #FEE2E2;
            color: #991B1B;
        }

        .pill-urgent {
            background-color: #FFEDD5;
            color: #9A3412;
        }

        .pill-normal {
            background-color: #DCFCE7;
            color: #166534;
        }

        .pill-verified {
            background-color: #DBEAFE;
            color: #1E40AF;
        }

        .pill-pending {
            background-color: #FEF3C7;
            color: #92400E;
        }

        /* Blood Drop Badge */
        .blood-badge {
            background-color: #DC2626;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 1.1rem;
            display: inline-block;
        }

        /* Buttons Styling */
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }

        /* Banner styling */
        .hero-banner {
            background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%);
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.3);
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: white;
            margin-bottom: 8px;
        }

        .hero-subtitle {
            font-size: 1.1rem;
            color: #FEE2E2;
            margin-bottom: 0px;
        }

        /* Match Score Badge */
        .match-high {
            color: #15803D;
            font-weight: 700;
            background: #DCFCE7;
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .match-medium {
            color: #B45309;
            font-weight: 700;
            background: #FEF3C7;
            padding: 4px 8px;
            border-radius: 6px;
        }

        </style>
    """, unsafe_allow_html=True)
