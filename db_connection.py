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

    def get_all_observations(self):
        conn = self._connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM weather_observations ORDER BY city_id;")
                return cur.fetchall()  
        except DatabaseError as e:
            print("Error fetching observations:", e)
            return []
        finally:  
            conn.close()

    def get_observation_by_id(self, obs_id):
        conn = self._connect()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM weather_observations WHERE city_id = %s;", (obs_id,),)
                return cur.fetchone()
        except DatabaseError as e:
            print("Error fetching observation by ID:", e)
            return None
        finally:
            conn.close()

    def insert_observation(self, weather):
        conn = self._connect()
        if not conn:
            return None

        try:
            with conn.cursor() as cur:
                query = """
                    INSERT INTO weather_observations (city, temperature, windspeed, latitude, longitude, observation_time)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
                """

                cur.execute(query, (
                    weather["city"],
                    weather["temperature"],
                    weather["windspeed"],
                    weather["latitude"],
                    weather["longitude"],
                    weather["observation_time"],
                ))

                new_record = cur.fetchone()
                conn.commit()
                return new_record

        except DatabaseError as e:
            print("Insert error:", e)
            conn.rollback()
            return None

        finally:
            conn.close()

    def update_observation(self, obs_id, temperature, windspeed):
        conn = self._connect()
        if not conn:
            return None

        try:
            with conn.cursor() as cur:
                query = """
                    UPDATE weather_observations
                    SET temperature = %s,
                        windspeed = %s
                    WHERE city_id = %s RETURNING *;
                """

                cur.execute(query, (temperature, windspeed, obs_id))

                # Check if record exists
                updated = cur.fetchone()
                if not updated:
                    print("No record found to update.")
                    return None

                conn.commit()
                return updated

        except DatabaseError as e:
            print("Update error:", e)
            conn.rollback()
            return None

        finally:
            conn.close()

    def delete_observation(self, obs_id):
        conn = self._connect()
        if not conn:
            return None

        try:
            with conn.cursor() as cur:
                query = """
                    DELETE FROM weather_observations
                    WHERE city_id = %s RETURNING *;
                """

                cur.execute(query, (obs_id,))
                deleted = cur.fetchone()

                if not deleted:
                    print("No record found to delete.")
                    return None

                conn.commit()
                return deleted

        except DatabaseError as e:
            print("Delete error:", e)
            conn.rollback()
            return None

        finally:
            conn.close()

if __name__ == "__main__":
    db = DatabaseManager()