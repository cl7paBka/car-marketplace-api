import psycopg2
from db.connection import get_db
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_db():
    logging.info("init_db Started")
    with get_db() as conn:
        logging.info("init_db Entered context manager get_db() as conn")

        cursor = conn.cursor()

        all_tables_queries = {create_table_users := """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            nickname VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL
        )
        """,

                              create_table_cars := """
        CREATE TABLE IF NOT EXISTS cars( 
            id SERIAL PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            brand VARCHAR(50) NOT NULL,
            model VARCHAR(50) NOT NULL,
            year INTEGER NOT NULL,
            price INTEGER NOT NULL,
            color VARCHAR(20) NOT NULL
        )
        """,
                              create_table_orders := """
        CREATE TABLE IF NOT EXISTS orders(
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            car_id INT NOT NULL,
            order_date DATE NOT NULL,
            status VARCHAR(50) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
        )                      
        """
                              }
        try:
            for create_table in all_tables_queries:
                cursor.execute(create_table)

            conn.commit()
            logging.info("All tables has been made successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            conn.rollback()
