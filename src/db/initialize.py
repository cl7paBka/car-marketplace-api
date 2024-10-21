from src.db.connection import get_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def init_db() -> None:
    """
    Initialize the database by creating necessary tables.

    Logs the creation status and rolls back in case of failure.
    """
    logging.info("Initializing database...")

    with get_db() as conn:
        cursor = conn.cursor()

        # SQL queries to create tables for users, cars, and orders
        tables = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                surname VARCHAR(50) NOT NULL,
                nickname VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS cars (
                id SERIAL PRIMARY KEY,
                type VARCHAR(50) NOT NULL,
                brand VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                year INTEGER NOT NULL,
                price INTEGER NOT NULL,
                color VARCHAR(20) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                car_id INT NOT NULL,
                order_date DATE NOT NULL,
                status VARCHAR(50) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
            )
            """
        ]

        try:
            # Execute each table creation query
            for table_query in tables:
                cursor.execute(table_query)

            conn.commit()
            logging.info("All tables created successfully.")
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            conn.rollback()
