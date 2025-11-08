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