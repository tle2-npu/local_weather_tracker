from models import Observation, NoteUpdate
from database import get_connection, create_table

create_table() 
 
def ingest_weather(city: str, country: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search"
    geo_res = requests.get(geo_url, params={"name": city, "country": country, "count": 1}).json()
    if "results" not in geo_res:
        raise HTTPException(status_code=404, detail="City not found")
    geo = geo_res["results"][0]
    lat, lon = geo["latitude"], geo["longitude"] 