from typing import List, Dict, Any
from utils.helpers import COMPATIBILITY_RECIPIENT_TO_DONORS, get_donor_eligibility
from database import get_request_by_id, get_all_donors, get_inventory_summary

def calculate_donor_match_score(donor: dict, request: dict) -> dict:
    """
    Calculate rule-based match score for a donor against a blood request.
    Returns dictionary with overall percentage, individual factor scores, and explanation.
    """
    required_bg = request["blood_group"]
    donor_bg = donor["blood_group"]
    req_city = request.get("location", request.get("hospital_city", "")).lower()
    donor_city = donor.get("city", "").lower()
    donor_area = donor.get("area", "").lower()

    # 1. Compatibility Check
    compatible_donors = COMPATIBILITY_RECIPIENT_TO_DONORS.get(required_bg, [])
    if donor_bg not in compatible_donors:
        return {
            "eligible": False,
            "match_score": 0,
            "reasons": ["Blood group incompatible"]
        }

    # Blood Group Score
    if donor_bg == required_bg:
        bg_score = 100
        bg_desc = f"Exact match ({donor_bg})"
    elif donor_bg == "O-":
        bg_score = 90
        bg_desc = "Universal donor (O-)"
    else:
        bg_score = 80
        bg_desc = f"Compatible match ({donor_bg} -> {required_bg})"

    # 2. Donor Availability Check
    if donor.get("availability", "AVAILABLE").upper() != "AVAILABLE":
        return {
            "eligible": False,
            "match_score": 0,
            "reasons": ["Donor currently marked unavailable"]
        }

    # 3. Donor Eligibility Check (Last Donation Date)
    eligibility_info = get_donor_eligibility(donor.get("last_donation"))
    if not eligibility_info["eligible"]:
        return {
            "eligible": False,
            "match_score": 0,
            "reasons": [eligibility_info["message"]]
        }
    eligibility_score = 100

    # 4. Location Match Score
    if req_city and donor_city and donor_city in req_city:
        if donor_area and donor_area in req_city:
            loc_score = 100
            loc_desc = f"Same area ({donor.get('area')}, {donor.get('city')})"
        else:
            loc_score = 85
            loc_desc = f"Same city ({donor.get('city')})"
    else:
        loc_score = 45
        loc_desc = f"Nearby location ({donor.get('city')})"

    # Overall Match Formula: 55% Blood Group + 30% Location + 15% Eligibility
    overall_score = round(0.55 * bg_score + 0.30 * loc_score + 0.15 * eligibility_score)

    return {
        "eligible": True,
        "match_score": overall_score,
        "bg_desc": bg_desc,
        "loc_desc": loc_desc,
        "eligibility_desc": eligibility_info["message"],
        "reasons": [bg_desc, loc_desc, "Eligible & Available"]
    }

def find_matched_donors_for_request(request_id: int) -> List[dict]:
    """Find and rank all compatible, eligible donors for a blood request."""
    request = get_request_by_id(request_id)
    if not request:
        return []

    donors = get_all_donors()
    matched_donors = []

    for donor in donors:
        match_result = calculate_donor_match_score(donor, request)
        if match_result["eligible"]:
            d_info = dict(donor)
            d_info["match_score"] = match_result["match_score"]
            d_info["match_details"] = match_result
            matched_donors.append(d_info)

    # Sort donors by highest match score
    matched_donors.sort(key=lambda x: x["match_score"], reverse=True)
    return matched_donors

def check_blood_bank_stock_for_request(blood_group: str) -> dict:
    """Check total blood bank stock available for a required blood group."""
    summary = get_inventory_summary()
    compatible_groups = COMPATIBILITY_RECIPIENT_TO_DONORS.get(blood_group, [])
    
    total_exact_units = 0
    total_compatible_units = 0

    for item in summary:
        bg = item["blood_group"]
        units = item["total_units"]
        if bg == blood_group:
            total_exact_units += units
        if bg in compatible_groups:
            total_compatible_units += units

    return {
        "exact_units": total_exact_units,
        "compatible_units": total_compatible_units,
        "has_stock": total_compatible_units > 0
    }
