import os
from dotenv import load_dotenv
import psycopg
from psycopg import OperationalError
from psycopg.rows import dict_row

load_dotenv()         # Load credentials .env file 

class DatabaseManager:
    def __init__(self):
        self.config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
        }    

    def _connect(self):
        """Establish a database connection"""
        try:
            return psycopg.connect(**self.config, row_factory=dict_row)
        except OperationalError as e:
            print("Database connection error:", e)
            return None

    def get_all_observations(self):
        query = "SELECT * FROM weather_observations ORDER BY city_id;"
        conn = self._connect()
        if not conn:
            return []

        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_observation_by_id(self, obs_id):
        query = "SELECT * FROM weather_observations WHERE city_id = %s;"
        conn = self._connect()
        if not conn:
            return None

        with conn.cursor() as cur:
            cur.execute(query, (obs_id,))
            row = cur.fetchone()

        conn.close()
        return row
    
    def insert_observation(self, weather):
        """
        weather = {
            'city': ...,
            'temperature': ...,
            'windspeed': ...,
            'latitude': ...,
            'longitude': ...,
            'observation_time': ...
        }
        """

        query = """
            INSERT INTO weather_observations 
                (city, temperature, windspeed, latitude, longitude, observation_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """

        conn = self._connect()
        if not conn:
            return None

        with conn.cursor() as cur:
            cur.execute(query, (
                weather["city"],
                weather["temperature"],
                weather["windspeed"],
                weather["latitude"],
                weather["longitude"],
                weather["observation_time"]
            ))
            new_row = cur.fetchone()
            conn.commit()

        conn.close()
        return new_row

    def update_observation(self, obs_id, temp, wind):
        query = """
            UPDATE weather_observations
            SET temperature = %s,
                windspeed = %s
            WHERE city_id = %s
            RETURNING *;
        """

        conn = self._connect()
        if not conn:
            return None

        with conn.cursor() as cur:
            cur.execute(query, (temp, wind, obs_id))
            updated = cur.fetchone()
            conn.commit()

        conn.close()
        return updated

    def delete_observation(self, obs_id):
        query = "DELETE FROM weather_observations WHERE city_id = %s RETURNING city_id;"

        conn = self._connect()
        if not conn:
            return None

        with conn.cursor() as cur:
            cur.execute(query, (obs_id,))
            deleted = cur.fetchone()
            conn.commit()

        conn.close()
        return deleted

if __name__ == "__main__":
    db = DatabaseManager()