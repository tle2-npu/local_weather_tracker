import requests

Geocoding_URL = "https://geocoding-api.open-meteo.com/v1/search" 
Weather_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true"

def fetch_weather_for_city(city, country):
    # 1. Fetch geocoding
    geo_params = {
        "name": city,
        "count": 1,
        "format": "json"
    }

    geo_response = requests.get(Geocoding_URL, params=geo_params, timeout=10)
    geo_data = geo_response.json()["results"][0]

    latitude = geo_data["latitude"]
    longitude = geo_data["longitude"]

    print("Geocoding status:", geo_response.status_code) 
    print("Geocoding URL:", geo_response.url) 

    # 2. Fetch weather
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    weather_response = requests.get(Weather_URL, params=weather_params, timeout=10)
    weather_data = weather_response.json()["current_weather"]

    print("Weather Status:", weather_response.status_code)
    print("Weather URL:", weather_response.url)

    return {
        "city": city,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
        "temperature_c": weather_data["temperature"],
        "windspeed_kmh": weather_data["windspeed"],
        "observation_time": weather_data["time"]
    }


if __name__ == "__main__":
    data = fetch_weather_for_city("Chicago", "US")
    print(data)

