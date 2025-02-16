from flask import Flask, render_template, request, jsonify
import googlemaps
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Google Maps API key
gmaps = googlemaps.Client(key="AIzaSyB9r0NBkTt_jE76o2yZgLBVcodw-JNpHXk")

# OpenWeatherMap API key
openweathermap_api_key = "0c27678ab120e7faac28a4845d981e6b"

# Function to get travel info
def get_travel_info(origin, destination):
    try:
        now = datetime.now()
        directions_result = gmaps.directions(
            origin,
            destination,
            mode="driving",
            departure_time=now,
            traffic_model="best_guess"
        )

        if directions_result:
            leg = directions_result[0]["legs"][0]
            travel_time_seconds = leg.get("duration_in_traffic", {}).get("value", leg["duration"]["value"])
            distance = leg["distance"]["text"]
            # Extracting the route steps, focusing on the main roads
            route_steps = []
            for step in leg["steps"]:
                # Simple way to extract road names from the instructions (remove HTML tags)
                road_name = step["html_instructions"]
                if "onto" in road_name:  # This is an indicator that we are switching roads
                    road_name = road_name.split(" onto ")[-1]
                route_steps.append(road_name)
            return travel_time_seconds, distance, route_steps
        else:
            print("No directions result found.")
            return None, None, None
    except Exception as e:
        print(f"Error fetching directions: {e}")
        return None, None, None

# Function to get weather info
def get_weather_condition(location):
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={openweathermap_api_key}&units=metric"
        response = requests.get(weather_url)
        
        if response.status_code == 200:
            weather_data = response.json()
            condition = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            return f"{condition.capitalize()}, {temperature}°C"
        else:
            print(f"Weather API Error: {response.status_code} - {response.json()}")
            return "Weather data unavailable"
    except Exception as e:
        print(f"Error fetching weather: {e}")
    return "Weather data unavailable"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to calculate travel time and traffic info
@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')
    print(f"Received origin: {origin}, destination: {destination}")  # Debugging line

    if not origin or not destination:
        return jsonify({'error': 'Origin and destination are required'}), 400

    travel_time, distance, route_steps = get_travel_info(origin, destination)
    weather_condition = get_weather_condition(origin)

    if travel_time is not None:
        return jsonify({
            'origin': origin,
            'destination': destination,
            'travel_time': travel_time,
            'distance': distance,
            'weather_condition': weather_condition,
            'route_steps': route_steps  # Include route steps in the response
        })
    else:
        return jsonify({'error': 'Could not calculate travel time'}), 500

if __name__ == '__main__':
    app.run(debug=True)
