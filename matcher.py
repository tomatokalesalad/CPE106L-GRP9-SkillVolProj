import sqlite3
from datetime import datetime
import uuid
from haversine import haversine
from location_utils import get_coordinates_from_address
from database import find_match, log_match
from map_viewer import open_match_map  # ✅ NEW: import Google Maps visualization

def match_request_to_volunteer(name, email, skill, location, availability):
    request_coords = get_coordinates_from_address(location)
    if not request_coords:
        return None

    volunteers = find_match(skill, location, availability)

    best_match = None
    shortest_distance = float("inf")

    for volunteer in volunteers:
        volunteer_name, volunteer_email, vol_location, vol_availability = volunteer
        vol_coords = get_coordinates_from_address(vol_location)
        if not vol_coords:
            continue

        distance = haversine(request_coords, vol_coords)
        if distance < shortest_distance:
            shortest_distance = distance
            best_match = volunteer

    if best_match:
        volunteer_name, volunteer_email, vol_location, vol_availability = best_match

        log_match(
            request_name=name,
            request_email=email,
            volunteer_name=volunteer_name,
            volunteer_email=volunteer_email,
            skill=skill,
            location=location,
            availability=availability,
            distance_km=shortest_distance
        )

        # ✅ NEW: Show map of the match
        volunteer_coords = get_coordinates_from_address(vol_location)
        open_match_map(request_coords, volunteer_coords)

        return volunteer_name, shortest_distance

    return None
