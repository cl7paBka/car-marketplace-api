from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME  # Переделать caps, потому что это константы

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # Example with SQLite, you can change it

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
