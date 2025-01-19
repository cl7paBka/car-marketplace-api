from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.utils.enums import TransmissionType, EngineType


# Input schemas
class CarCreateSchema(BaseModel):
    brand: str
    model: str
    price: int
    year: int
    color: str
    mileage: int
    transmission: TransmissionType
    engine: EngineType
    vin_number: str


class CarUpdateSchema(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    price: Optional[int] = None
    year: Optional[int] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    transmission: Optional[TransmissionType] = None
    engine: Optional[EngineType] = None
    vin_number: Optional[str] = None


class CarSchema(BaseModel):
    id: int
    brand: str
    model: str
    price: int
    year: int
    color: str
    mileage: int
    transmission: TransmissionType
    engine: EngineType
    vin_number: str
    created_at: datetime
    updated_at: Optional[datetime] = None

