from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.db.models import EngineType, TransmissionType


class CarCreate(BaseModel):
    """
    Schema for creating a new car entry.

    All fields are required to ensure the creation of a valid car object.
    """
    price: int
    brand: str
    model: str
    year: int
    color: str
    mileage: int
    transmission: TransmissionType
    engine: EngineType
    vin_number: str


class CarInfo(BaseModel):
    """
    Schema for updating or displaying car information.

    All fields are optional to allow partial updates or selective display of data.
    """
    price: Optional[int] = None
    brand: Optional[int] = None
    model: Optional[int] = None
    year: Optional[int] = None
    color: Optional[int] = None
    mileage: Optional[int] = None
    transmission: Optional[TransmissionType] = None
    engine: Optional[EngineType] = None
    vin_number: Optional[str] = None


class CarInDB(BaseModel):
    """
    Schema for representing a car as stored in the database.

    Includes a unique identifier for each car.
    """
    id: int
    price: int
    brand: str
    model: str
    year: int
    color: str
    mileage: int
    transmission: TransmissionType
    engine: EngineType
    price: int
    vin_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
