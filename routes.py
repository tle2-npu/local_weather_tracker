from flask import Flask, render_template, request
from main import fetch_weather_for_city
from db_connection import DatabaseManager

app = Flask(__name__)
db = DatabaseManager()

@app.route('/')
def home():
    return render_template('index.html')

# Get all  
@app.route('/observations')
def list_observations():
    rows = db.get_all_observations()
    return render_template('observation.html', observations=rows)

# Get by ID  
@app.route('/observations/<int:obs_id>')
def observation_detail(obs_id):
    row = db.get_observation_by_id(obs_id)
    return render_template('observation_id.html', record=row)

# Post 
@app.route('/ingest', methods=['GET', 'POST'])
def ingest_city():
    if request.method == 'POST':
        city = request.form.get('city')
        
        # call API
        weather = fetch_weather_for_city(city)
        if not weather:
            return 'City not found. Please enter a valid city name.'

        # insert database
        new_row = db.insert_observation(weather)

        return render_template("ingest.html", new_record=new_row)

    return render_template("ingest.html")

# Update temp & wind
@app.route('/observations/<int:obs_id>/update', methods=['GET', 'POST'])
def update_observation(obs_id):
    if request.method == 'POST':
        temp = request.form.get('temperature')
        wind = request.form.get('windspeed')

        updated = db.update_observation(obs_id, temp, wind)
        return render_template('update.html', updated=updated)

    row = db.get_observation_by_id(obs_id)
    return render_template('update.html', record=row)

# DELETE 
@app.route('/observations/<int:obs_id>/delete', methods=['GET', 'POST'])
def delete_observation(obs_id):
    if request.method == 'POST':
        deleted = db.delete_observation(obs_id)
        return render_template('delete.html', deleted=deleted)

    row = db.get_observation_by_id(obs_id)
    return render_template('delete.html', record=row)

if __name__ == '__main__':
    app.run(debug=True)
