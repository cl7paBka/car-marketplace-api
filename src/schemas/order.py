from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.db.models import OrderStatus


class OrderCreate(BaseModel):
    """
    Schema for creating a new order.

    All fields are required to ensure the creation of a valid order object.
    """
    status: OrderStatus
    user_id: int
    car_id: int
    salesperson_id: int
    comments: str


class OrderInfo(BaseModel):
    """
    Schema for updating or displaying order information.

    All fields are optional for flexible updates or display.
    """
    status: Optional[OrderStatus] = None
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    salesperson_id: Optional[int] = None
    comments: Optional[str] = None

    class Config:
        from_attributes = True


class OrderInDB(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: OrderStatus
    user_id: int
    car_id: int
    salesperson_id: int
    comments: str

    class Config:
        from_attributes = True
