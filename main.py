import requests

Geocoding_URL = "https://geocoding-api.open-meteo.com/v1/search" 
Weather_URL = "https://api.open-meteo.com/v1/forecast?current_weather=true" 

city = "Chicago"  
geo_params = {"name": city, "count": 1,} 
