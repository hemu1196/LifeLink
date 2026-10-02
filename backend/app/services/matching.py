from typing import List, Dict, Any
from backend.app.services.compatibility import COMPATIBILITY_RECIPIENT_TO_DONORS
from backend.app.services.eligibility import get_donor_eligibility

def calculate_donor_match_score(donor_dict: dict, req_bg: str, req_location: str, req_city: str) -> dict:
    """Calculate rule-based match score for a donor against a blood request."""
    donor_bg = donor_dict.get("blood_group")
    donor_city = (donor_dict.get("city") or "").lower()
    donor_area = (donor_dict.get("area") or "").lower()
    target_city = req_city.lower() if req_city else ""
    target_loc = req_location.lower() if req_location else ""

    # 1. Compatibility Check
    compatible_donors = COMPATIBILITY_RECIPIENT_TO_DONORS.get(req_bg, [])
    if donor_bg not in compatible_donors:
        return {"eligible": False, "match_score": 0, "reasons": ["Incompatible blood group"]}

    # Blood Group Score
    if donor_bg == req_bg:
        bg_score = 100
        bg_desc = f"Exact match ({donor_bg})"
    elif donor_bg == "O-":
        bg_score = 90
        bg_desc = "Universal donor (O-)"
    else:
        bg_score = 80
        bg_desc = f"Compatible match ({donor_bg} -> {req_bg})"

    # 2. Availability Check
    if (donor_dict.get("availability") or "AVAILABLE").upper() != "AVAILABLE":
        return {"eligible": False, "match_score": 0, "reasons": ["Donor currently marked unavailable"]}

    # 3. Eligibility Check
    eligibility_info = get_donor_eligibility(donor_dict.get("last_donation"))
    if not eligibility_info["eligible"]:
        return {"eligible": False, "match_score": 0, "reasons": [eligibility_info["message"]]}
    eligibility_score = 100

    # 4. Location Score
    if target_city and donor_city and donor_city in target_city:
        if donor_area and donor_area in target_loc:
            loc_score = 100
            loc_desc = f"Same area ({donor_dict.get('area')}, {donor_dict.get('city')})"
        else:
            loc_score = 85
            loc_desc = f"Same city ({donor_dict.get('city')})"
    else:
        loc_score = 45
        loc_desc = f"Nearby location ({donor_dict.get('city')})"

    overall_score = round(0.55 * bg_score + 0.30 * loc_score + 0.15 * eligibility_score)

    return {
        "eligible": True,
        "match_score": overall_score,
        "bg_desc": bg_desc,
        "loc_desc": loc_desc,
        "eligibility_desc": eligibility_info["message"],
        "reasons": [bg_desc, loc_desc, "Eligible & Available"]
    }
