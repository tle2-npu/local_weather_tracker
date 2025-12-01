import requests
import time 

Geocoding_URL = "https://geocoding-api.open-meteo.com/v1/search" 
Weather_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true"

retries = 3 

def simple_get(url, params=None):
    for attempt in range(retries):              
        try:
            return requests.get(url, params=params, timeout=10)
        except requests.exceptions.RequestException:
            print("Request failed. Retrying...")
            time.sleep(1)                 
    return None                           

def fetch_weather_for_city(city):
    # Get latitude/longitude 
    geo_params = {
        "name": city,
        "count": 1,
    }

    geo_response = simple_get(Geocoding_URL, params=geo_params)

    if not geo_response:
        print("Geocoding failed")
        return None
    
    geo_json = geo_response.json()

    if "results" not in geo_json:
        print(f"No geocoding results for {city}")
        return None

    geo_data = geo_json["results"][0]

    latitude = geo_data["latitude"]
    longitude = geo_data["longitude"]
    country = geo_data.get("country", "Unknown")
   
    # Get current weather info 
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    weather_response = simple_get(Weather_URL, params=weather_params)

    if not weather_response:
        print("Weather API failed")
        return None
    
    weather_data = weather_response.json()["current_weather"]
    
    return {
        "city": city,
        "country": country,
        "temperature": weather_data["temperature"],
        "windspeed": weather_data["windspeed"],
        "latitude": latitude,
        "longitude": longitude,
        "observation_time": weather_data["time"]
    }

if __name__ == "__main__":
    data = fetch_weather_for_city("Tokyo")
    print(data)