import psycopg2
from db.connection import get_db
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_db():
    logging.info("init_db Started")
    with get_db() as conn:
        logging.info("init_db Entered context manager get_db() as conn")

        cursor = conn.cursor()

        create_table_cars = """
        CREATE TABLE IF NOT EXISTS cars(
            id SERIAL PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            brand VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            year INTEGER NOT NULL,
            price INTEGER NOT NULL,
            color VARCHAR(20) NOT NULL
        )
        """

        try:
            cursor.execute(create_table_cars)
            conn.commit()
            logging.info("Table cars has been made successfully.")
        except Exception as e:
            print(f"Error creating table cars: {e}")
            conn.rollback()
