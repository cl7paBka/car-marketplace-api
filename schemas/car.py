from pydantic import BaseModel
from typing import Optional


class CarCreate(BaseModel):
    price: int
    color: str
    year: int
    type: str
    model: str
    brand: str


class CarInfo(BaseModel):
    price: Optional[int] = None
    color: Optional[str] = None
    year: Optional[int] = None
    type: Optional[str] = None
    model: Optional[str] = None
    brand: Optional[str] = None


class CarInDB(CarInfo):
    car_id: int

