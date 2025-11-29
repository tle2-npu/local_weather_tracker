from flask import Flask, render_template, jsonify, request 
from main import fetch_weather_for_city
from db_connection import DatabaseManager

app = Flask(__name__)
db = DatabaseManager()

@app.route('/')
def home():
    return render_template("index.html", title="Home")

# POST - Fetches live weather, saves it, returns record
@app.route('/ingest', methods=['POST'])
def ingest_weather():
    data = request.get_json()
    city = data.get("city")
    country = data.get("country", "N/A")

    obs = fetch_weather_for_city(city, country)
    if not obs:
        return jsonify({"error": "Failed to fetch weather"}), 500

    saved = db.insert_observation(obs)
    return jsonify({
        "message": "Weather data saved successfully",
        "record_id": saved.city_id
    }), 201

# GET - Retrieves all stored observations
@app.route('/observations', methods=['GET'])
def list_observations():
    records = db.get_all_observations()
    return render_template('observation.html', title="All Observations", records=records)

# GET - Retrieves a specific observation by ID
@app.route('/observations/<int:obs_id>', methods=['GET'])
def show_observation(obs_id):
    record = db.get_observation_by_id(obs_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    return render_template('observation_id.html', title=f"Observation {obs_id}", record=record)

# PUT - Updates the notes field of an observation
@app.route('/observations/<int:obs_id>', methods=['PUT'])
def update_observation(obs_id):
    data = request.get_json()
    lat = data.get("latitude")
    lon = data.get("longitude")

    updated = db.update_location(obs_id, lat, lon)
    if updated == 0:
        return jsonify({"error": "Update failed"}), 400

    return jsonify({"message": "Updated successfully"}), 200

# DELETE - Deletes an observation from DB 
@app.route('/observations/<int:obs_id>', methods=['DELETE'])
def delete_observation(obs_id):
    deleted = db.delete_observation(obs_id)
    if deleted == 0:
        return jsonify({"error": "Delete failed"}), 400

    return jsonify({"message": "Deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
