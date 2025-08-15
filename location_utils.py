import re

# Simple dictionary for common PH cities; extend as needed
CITY_TO_COORDS = {
    "Manila": (14.5995, 120.9842),
    "Quezon": (14.6760, 121.0437),
    "Makati": (14.5547, 121.0244),
    "Alabang": (14.4182, 121.0421),
    "Pasay": (14.5377, 121.0008),
    "Pasig": (14.5764, 121.0851),
    "Taguig": (14.5176, 121.0509),
}

def get_coordinates_from_address(address: str):
    """Return (lat, lon) from 'lat,lon' text or known city names; else None."""
    if not address:
        return None
    s = address.strip().lower()
    # pattern like "14.60, 121.03"
    m = re.match(r"^\s*(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)\s*$", s)
    if m:
        return (float(m.group(1)), float(m.group(3)))
    return CITY_TO_COORDS.get(s)
