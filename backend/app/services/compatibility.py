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

def is_blood_compatible(donor_group: str, recipient_group: str) -> bool:
    """Check if donor blood group is compatible with recipient blood group."""
    compatible_donors = COMPATIBILITY_RECIPIENT_TO_DONORS.get(recipient_group, [])
    return donor_group in compatible_donors
