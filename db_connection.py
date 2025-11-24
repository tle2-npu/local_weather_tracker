import psycopg

class DatabaseConnection:
        
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    # Connect 
    def connect(self):
        try:
            self.conn = psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return self.conn
        except Exception as e:
            print("Database connection error:", str(e))
            return None

    def close(self):
        """Close the connection safely"""
        if self.conn:
            self.conn.close()