from models import Observation, NoteUpdate
from database import get_connection, create_table
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Local Weather Tracker")
create_table() 
 
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

    cur.close()
    conn.close()

# GET 
@app.get("/observations")
def get_all_observations(): 
