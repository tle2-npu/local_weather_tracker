import os
from dotenv import load_dotenv
import psycopg
from psycopg.errors import OperationalError, DatabaseError
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
        
    def _execute(self, query, params=None, fetch="all"):
        """eliminates repetition"""

        conn = self._connect()
        if not conn:
            return None

        try:
            with conn.cursor() as cur:
                cur.execute(query, params)

                if fetch == "one":
                    result = cur.fetchone()
                elif fetch == "none":
                    result = None
                else:
                    result = cur.fetchall()

                conn.commit()
                return result

        except DatabaseError as e:
            print("DatabaseError:", e)
            conn.rollback()
            return None

        finally:
            conn.close()

    # CRUD 
    def get_all_observations(self):
        return self._execute("SELECT * FROM weather_observations ORDER BY city_id;")

    def get_observation_by_id(self, obs_id):
        return self._execute(
            "SELECT * FROM weather_observations WHERE city_id = %s;",
            (obs_id,),
            fetch="one"
        )

    def insert_observation(self, w):
        return self._execute(
            """
            INSERT INTO weather_observations (city, temperature, windspeed, latitude, longitude, observation_time)
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING *;
            """,
            (w["city"], w["temperature"], w["windspeed"], w["latitude"], w["longitude"], w["observation_time"]),
            fetch="one"
        )

    def update_observation(self, obs_id, temp, wind):
        return self._execute(
            """
            UPDATE weather_observations
            SET temperature=%s, windspeed=%s
            WHERE city_id=%s
            RETURNING *;
            """,
            (temp, wind, obs_id),
            fetch="one"
        )

    def delete_observation(self, obs_id):
        return self._execute(
            """
            DELETE FROM weather_observations WHERE city_id=%s
            RETURNING *;
            """,
            (obs_id,),
            fetch="one"
        )    

if __name__ == "__main__":
    db = DatabaseManager()