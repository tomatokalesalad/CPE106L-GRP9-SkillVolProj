from location_utils import geocode_address, calculate_distance

# Test geocoding
lat, lng = geocode_address("Pasay City, Philippines")
print(f"Coordinates of Pasay: {lat}, {lng}")

# Test distance calculation
distance = calculate_distance("Pasay City, Philippines", "Makati City, Philippines")
print(f"Distance between Pasay and Makati: {distance:.2f} km")
