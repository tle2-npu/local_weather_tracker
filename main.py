import requests

Geocoding_URL = "https://geocoding-api.open-meteo.com/v1/search" 
Weather_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true" 

city = "Chicago"  

geo_params = {
    "name": city, 
    "count": 1} 

response = requests.get(Geocoding_URL, params=geo_params) 
print("Geocoding status:", response.status_code) 
print("Geocoding URL:", response.url) 

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
    }
weather_response = requests.get(Weather_URL, params=weather_params)
print("Weather Status:", weather_response.status_code)
print("Weather URL:", weather_response.url)
