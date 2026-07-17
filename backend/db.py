import psycopg2


def get_db_connection():

    conn = psycopg2.connect(
        host="localhost",
        database="attendance_db",
        user="postgres",
        password="Yassu16@",
        port="5432"
    )

    return conn