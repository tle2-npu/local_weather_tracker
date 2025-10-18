import requests, json 

Geocoding_URL = "https://geocoding-api.open-meteo.com/v1/search" 
Weather_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true" 

city = "Chicago"  

geo_params = {
    "name": city, 
    "count": 1,
    "format": "json"
    } 

response = requests.get(Geocoding_URL, params=geo_params, timeout=10) 
print("Geocoding status:", response.status_code) 
print("Geocoding URL:", response.url) 

data = response.json()
latitude = data["results"][0]["latitude"]
longitude = data["results"][0]["longitude"] 

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

print(f"City: {city}")
print(f"Temperature: {temperature}")
print(f"Windspeed: {windspeed}")
print(f"Observation time: {observation_time}")