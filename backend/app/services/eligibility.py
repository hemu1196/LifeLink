from datetime import datetime, timedelta

def get_donor_eligibility(last_donation_str: str, min_days: int = 90) -> dict:
    """Calculate donor eligibility based on last donation date."""
    if not last_donation_str:
        return {
            "eligible": True,
            "days_since": 999,
            "days_remaining": 0,
            "next_eligible_date": "Immediately",
            "message": "Eligible to donate! No previous donation logged."
        }
    
    try:
        last_date = datetime.strptime(last_donation_str, "%Y-%m-%d").date()
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
