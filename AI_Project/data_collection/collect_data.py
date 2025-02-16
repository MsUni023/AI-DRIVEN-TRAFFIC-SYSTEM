##collect_data.py
import googlemaps
from datetime import datetime

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key="AIzaSyB9r0NBkTt_jE76o2yZgLBVcodw-JNpHXk")

# Function to get travel time with real-time traffic data
def get_travel_time(origin, destination):
    # Get the current time
    now = datetime.now()

    # Get directions with traffic considerations
    directions_result = gmaps.directions(
        origin,
        destination,
        mode="driving",
        departure_time=now,
        traffic_model="best_guess"
    )

    # Extract travel time in seconds and convert to minutes
    if directions_result:
        travel_time_seconds = directions_result[0]["legs"][0]["duration_in_traffic"]["value"]
        travel_time_minutes = travel_time_seconds / 60
        return travel_time_minutes
    else:
        return None

# Example usage
origin = "Maseno, Kisumu"
destination = "Odeon, Nairobi"

travel_time = get_travel_time(origin, destination)

if travel_time:
    print(f"Estimated travel time: {travel_time:.2f} minutes")
else:
    print("Could not calculate travel time.")

