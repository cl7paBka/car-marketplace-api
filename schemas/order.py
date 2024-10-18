from pydantic import BaseModel
from typing import Optional
from datetime import date

class OrderCreate(BaseModel):
    user_id: int
    car_id: int
    order_date: date
    status: str


class OrderInfo(BaseModel):
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    order_date: Optional[date] = None
    status: Optional[str] = None


class OrderInDB(OrderInfo):
    id: int
