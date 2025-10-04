from fastapi import FastAPI, HTTPException
import sqlite3
import requests

app = FastAPI(title="Local Weather Tracker")

DB_FILE = "weather.db"
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute()
    conn.commit()
    conn.close()

init_db()  

# POST  
@app.post("/ingest")
def ingest_weather(city: str, country: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search"
    geo_res = requests.get(geo_url, params={"name": city, "country": country, "count": 1}).json()
    if "results" not in geo_res:
        raise HTTPException(status_code=404, detail="City not found")
    geo = geo_res["results"][0]
    lat, lon = geo["latitude"], geo["longitude"] 

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_res = requests.get(weather_url, params={"latitude": lat, "longitude": lon, "current_weather": True}).json()
    cw = weather_res["current_weather"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(city, country, lat, lon, cw["temperature"], cw["windspeed"], cw["time"])
    cur.close()
    conn.close()
    conn.commit()

    obs_id = cur.lastrowid

    return {
        "id": obs_id,
        "city": city,
        "country": country,
        "latitude": lat,
        "longitude": lon,
        "temperature": cw["temperature"],
        "windspeed": cw["windspeed"],
        "observation_time": cw["time"],
        "notes": None
    }

# GET 
@app.get("/observations")
def get_observations(): 
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM observations")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

@app.get("/observations/{obs_id}") 