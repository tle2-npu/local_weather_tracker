import os
from dotenv import load_dotenv
import psycopg
from psycopg import OperationalError
from datetime import datetime 

load_dotenv()         # Load variables .env file 

class WeatherObservation:
    """WeatherObservation class maps to weather_observations table"""

    def __init__(self, city, country="N/A", temperature=None, windspeed=None,
                 latitude=None, longitude=None, observation_time=None, city_id=None):
        self.city_id = city_id
        self.city = city
        self.country = country
        self.temperature = temperature
        self.windspeed = windspeed
        self.latitude = latitude
        self.longitude = longitude
        self.observation_time = observation_time or datetime.now()

    def __repr__(self):
        return (f"<WeatherObservation(id={self.city_id}, city='{self.city}', temp={self.temperature}, "
                f"windspeed={self.windspeed}, lat={self.latitude}, lon={self.longitude}, "
                f"time={self.observation_time})>")

class DatabaseManager:
    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")    

    def _connect(self):
        try:
            conn = psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except OperationalError as e:
            print("Database connection error:", e)
            return None 