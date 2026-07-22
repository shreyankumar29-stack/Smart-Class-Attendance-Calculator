import os
import psycopg2


def get_db_connection():

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "attendance_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "Yassu16@"),
        port=os.getenv("DB_PORT", "5432")
    )

    return conn