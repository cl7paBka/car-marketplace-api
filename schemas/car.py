from pydantic import BaseModel
from typing import Optional


class CarCreate(BaseModel):
    """
    Schema for creating a new car entry.

    All fields are required to ensure the creation of a valid car object.
    """
    price: int
    color: str
    year: int
    type: str
    model: str
    brand: str


class CarInfo(BaseModel):
    """
    Schema for updating or displaying car information.

    All fields are optional to allow partial updates or selective display of data.
    """
    price: Optional[int] = None
    color: Optional[str] = None
    year: Optional[int] = None
    type: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None


class CarInDB(CarInfo):
    """
    Schema for representing a car as stored in the database.

    Includes a unique identifier for each car.
    """
    car_id: int
