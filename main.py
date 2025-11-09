import requests

Geocoding_URL = "https://geocoding-api.open-meteo.com/v1/search" 

city = "Houston"  

geo_params = {
    "name": city, 
    "count": 1,
    "format": "json"
    } 

response = requests.get(Geocoding_URL, params=geo_params, timeout=10) 
print("Geocoding status:", response.status_code) 
print("Geocoding URL:", response.url) 

data = response.json()
result = data["results"][0]
geo_id = result["id"]
country = result["country"]
latitude = result["latitude"]
longitude = result["longitude"] 

Weather_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true"

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
    }

weather_response = requests.get(Weather_URL, params=weather_params, timeout=10)
print("Weather Status:", weather_response.status_code)
print("Weather URL:", weather_response.url)

weather_data = weather_response.json()
current_weather = weather_data["current_weather"]

temperature = current_weather["temperature"]
windspeed = current_weather["windspeed"]
observation_time = current_weather["time"]

print("---WEATHER REPORT---")
print(f"City: {city}")
print(f"Country: {country}")
print(f"Temperature: {temperature}")
print(f"Windspeed: {windspeed}")
print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")
print(f"Observation time: {observation_time}") 

from flask import Flask, render_template, jsonify

app = Flask(__name__)

# POST - Fetches live weather, saves it, returns record
@app.route('/ingest', methods=['POST'])
def ingest_weather():
    return jsonify({'message': "Ingest endpoint"}), 200

# GET - Retrieves all stored observations
@app.route('/observations', methods=['GET'])
def list_observations():
    # 2 sample records
    records = [
  {"city": "Chicago", "temp": 19.2, "wind": 12.5},
  {"city": "Houston", "temp": 22.2, "wind": 7.3}
]
    return render_template('observation.html', title="Observation", records=records)

# GET - Retrieves a specific observation by ID
@app.route('/observations/<int:obs_id>', methods=['GET'])
def show_observation(obs_id):
    return render_template('observation_id.html', obs_id=obs_id)

# PUT - Updates the notes field of an observation
@app.route('/observations/<int:obs_id>', methods=['PUT'])
def update_observation(obs_id):
    return jsonify({'message': f"Update for ID {obs_id}"}), 200

# DELETE - Deletes an observation from DB 
@app.route('/observations/<int:obs_id>', methods=['DELETE'])
def delete_observation(obs_id):
    return jsonify({'message': f"Delete for ID {obs_id}"}), 200

if __name__ == '__main__':
    app.run(debug=True) 
