import os
from dotenv import load_dotenv
import psycopg

load_dotenv()         # Load variables .env file 

class DatabaseManager:

    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.conn = None
        self.cursor = None

        self.connect()

    def connect(self):
        try:
            self.conn = psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL successfully")
        except Exception as e:
            print("Database connection error:", str(e))