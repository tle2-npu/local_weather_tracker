import sqlite3

DB_FILE = "weather.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # to get dict-like rows
    return conn

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    conn.commit()
    cur.close()
    conn.close()