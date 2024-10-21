import psycopg2
import logging
import os
from typing import Any

# Set up logging format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Retrieve database connection parameters from environment variables
db_password = os.getenv("DATABASE_PASSWORD")
db_host = os.getenv("DATABASE_HOST", "localhost")
db_name = os.getenv("DATABASE_NAME", "postgres")
db_user = os.getenv("DATABASE_USER", "postgres")
db_port = os.getenv("DATABASE_PORT", "5432")


def get_db() -> Any:
    """
    Establish and return a connection to the PostgreSQL database.

    Uses environment variables for database credentials. Connection is returned in non-autocommit mode.
    """
    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password,
        port=db_port
    )
    conn.autocommit = False  # Transactions won't commit automatically
    return conn
