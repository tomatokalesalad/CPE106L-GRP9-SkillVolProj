import webbrowser
from urllib.parse import urlencode

def open_match_map(request_coords, volunteer_coords):
    base_url = "https://www.google.com/maps/dir/?"
    params = {
        "api": 1,
        "origin": f"{request_coords[0]},{request_coords[1]}",
        "destination": f"{volunteer_coords[0]},{volunteer_coords[1]}",
        "travelmode": "driving"
    }

    map_url = base_url + urlencode(params)
    webbrowser.open(map_url)
