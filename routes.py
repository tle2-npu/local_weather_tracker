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
