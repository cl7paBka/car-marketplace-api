import os
from dotenv import load_dotenv

load_dotenv()

# Loading from .env file for test db
TEST_DB_PASSWORD = os.getenv("TEST_DATABASE_PASSWORD")
TEST_DB_HOST = os.getenv("TEST_DATABASE_HOST", "car-marketplace-test-db")
TEST_DB_NAME = os.getenv("TEST_DATABASE_NAME", "car-marketplace-test")
TEST_DB_USER = os.getenv("TEST_DATABASE_USER", "postgres")
TEST_DB_PORT = os.getenv("TEST_DATABASE_PORT", "5433")

# Test data for users
USER_CUSTOMER = {
    "name": "Lera",
    "surname": "Novikova",
    "email": "LeraNovik33@yandex.ru",
    "role": "customer"
}

USER_MANAGER = {
    "name": "Boris",
    "surname": "Sokolov",
    "email": "SokolBorya21@gmail.com",
    "role": "manager"
}

INVALID_ROLE_USER = {
    "name": "Invalid",
    "surname": "Role",
    "email": "invalid-role@example.com",
    "role": "supervisor"  # Not in valid enum
}

MISSING_FIELDS_USER = {
    # "name" is deleted to simulate missing required fields
    "surname": "NoName",
    "email": "missing@example.com",
    "role": "customer"
}

# Test data for cars
CAR_CREATE_VALID = {
    "brand": "Toyota",
    "model": "Camry",
    "price": 30000,
    "year": 2020,
    "color": "Blue",
    "mileage": 15000,
    "transmission": "automatic",  # valid values: 'automatic', 'manual'
    "engine": "gasoline",         # valid values: 'electric', 'gasoline', 'diesel'
    "vin_number": "VIN1234567890"
}

CAR_CREATE_ANOTHER = {
    "brand": "Honda",
    "model": "Civic",
    "price": 25000,
    "year": 2019,
    "color": "Red",
    "mileage": 20000,
    "transmission": "manual",     # valid values: 'automatic', 'manual'
    "engine": "gasoline",         # valid values: 'electric', 'gasoline', 'diesel'
    "vin_number": "VIN0987654321"
}

CAR_UPDATE_VALID = {
    "color": "Black",
    "mileage": 16000
}