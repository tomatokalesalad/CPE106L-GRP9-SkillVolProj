import requests
import os

# Set your API key here or load it from environment variable
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyDCgCVVgTMnEk8i8lCBDgN2aRXnC0KG-Hk")

def get_coordinates_from_address(address):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,   # ←✅ FIXED: removed the typo `tis this correct`
        "key": GOOGLE_MAPS_API_KEY
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print("No location found.")
    else:
        print("Error in API request:", response.status_code)

    return None
