import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="property_app",
        user="postgres",
        password="harsh",
        port=5432
    )
    return conn
