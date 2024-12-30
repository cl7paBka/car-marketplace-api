from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from src.utils.enums import OrderStatus


class OrderCreateSchema(BaseModel):
    user_id: int
    car_id: int
    salesperson_id: int
    status: OrderStatus
    comments: str


class OrderUpdateSchema(BaseModel):
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    salesperson_id: Optional[int] = None
    status: Optional[OrderStatus] = None
    comments: Optional[str] = None


class OrderSchema(BaseModel):
    id: int
    user_id: int
    car_id: int
    salesperson_id: int
    status: OrderStatus
    comments: str
    created_at: datetime
    updated_at: Optional[datetime] = None
