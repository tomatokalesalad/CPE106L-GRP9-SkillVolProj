from database import find_match, log_match
from haversine import haversine

# Dummy coordinates — add more cities as needed
city_coords = {
    "Manila": (14.5995, 120.9842),
    "Quezon City": (14.6760, 121.0437),
    "Pasay": (14.5378, 121.0014),
    "Makati": (14.5547, 121.0244),
}

def get_coordinates(city):
    return city_coords.get(city)

def match_request_to_volunteer(name, email, skill, location, availability):
    request_coords = get_coordinates(location)
    if not request_coords:
        return None

    # Get all volunteers who match skill/availability
    volunteers = find_match(skill, location, availability)

    best_match = None
    shortest_distance = float("inf")

    for volunteer in volunteers:
        volunteer_name, volunteer_email, vol_location, vol_availability = volunteer
        vol_coords = get_coordinates(vol_location)
        if not vol_coords:
            continue

        distance = haversine(request_coords, vol_coords)
        if distance < shortest_distance:
            shortest_distance = distance
            best_match = volunteer

    if best_match:
        # Destructure best volunteer info
        volunteer_name, volunteer_email, vol_location, vol_availability = best_match

        # Log the match to DB
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

        return volunteer_name, shortest_distance

    return None
