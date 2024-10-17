import psycopg2
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db_password = os.getenv("database_password")
db_host = os.getenv("database_host")
db_name = os.getenv("database_name")
db_user = os.getenv("database_user")
db_port = os.getenv("database_port")


def get_db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password=db_password,
        port=5432
    )
    conn.autocommit = False
    return conn
