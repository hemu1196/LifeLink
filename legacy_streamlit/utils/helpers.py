import hashlib
from datetime import datetime, timedelta

# Blood Compatibility Rules
# Keys: Recipient blood group -> Values: List of compatible donor blood groups
COMPATIBILITY_RECIPIENT_TO_DONORS = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
}

# Keys: Donor blood group -> Values: List of compatible recipient blood groups
COMPATIBILITY_DONOR_TO_RECIPIENTS = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"]
}

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a standard salt."""
    salt = "lifelink_secret_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def is_blood_compatible(donor_group: str, recipient_group: str) -> bool:
    """Check if donor blood group is compatible with recipient blood group."""
    compatible_donors = COMPATIBILITY_RECIPIENT_TO_DONORS.get(recipient_group, [])
    return donor_group in compatible_donors

def get_donor_eligibility(last_donation_str: str, min_days: int = 90) -> dict:
    """
    Calculate donor eligibility based on last donation date.
    Returns dict with status, days_since, days_remaining, next_eligible_date.
    """
    if not last_donation_str:
        return {
            "eligible": True,
            "days_since": 999,
            "days_remaining": 0,
            "next_eligible_date": "Immediately",
            "message": "Eligible to donate! No previous donation logged."
        }
    
    try:
        if isinstance(last_donation_str, str):
            last_date = datetime.strptime(last_donation_str, "%Y-%m-%d").date()
        else:
            last_date = last_donation_str
            
        today = datetime.now().date()
        days_since = (today - last_date).days
        
        if days_since >= min_days:
            return {
                "eligible": True,
                "days_since": days_since,
                "days_remaining": 0,
                "next_eligible_date": "Today",
                "message": f"Eligible to donate! ({days_since} days since last donation)"
            }
        else:
            days_remaining = min_days - days_since
            next_date = today + timedelta(days=days_remaining)
            return {
                "eligible": False,
                "days_since": days_since,
                "days_remaining": days_remaining,
                "next_eligible_date": next_date.strftime("%Y-%m-%d"),
                "message": f"Not eligible yet. Please wait {days_remaining} more days (Next eligible: {next_date.strftime('%d %b %Y')})"
            }
    except Exception:
        return {
            "eligible": True,
            "days_since": 999,
            "days_remaining": 0,
            "next_eligible_date": "Today",
            "message": "Eligible to donate."
        }

def get_priority_color(priority: str) -> str:
    """Return badge color for priority levels."""
    priority_upper = priority.upper()
    if priority_upper == "CRITICAL":
        return "#DC2626"  # Red
    elif priority_upper == "URGENT":
        return "#EA580C"  # Orange
    else:
        return "#16A34A"  # Green
