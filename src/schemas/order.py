from pydantic import BaseModel
from typing import Optional
from datetime import date


class OrderCreate(BaseModel):
    """
    Schema for creating a new order.

    All fields are required for the creation of a valid order object.
    """
    user_id: int
    car_id: int
    order_date: date
    status: str


class OrderInfo(BaseModel):
    """
    Schema for updating or displaying order information.

    All fields are optional for flexible updates or display.
    """
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    order_date: Optional[date] = None
    status: Optional[str] = None


class OrderInDB(OrderInfo):
    """
    Schema representing an order stored in the database.

    Includes a unique identifier for each order.
    """
    id: int
