from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.db.models import Order
from src.schemas.order import OrderCreate, OrderInDB, OrderInfo
from typing import Optional, List


class OrderRepository:
    """
    Repository for managing user-related database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: OrderCreate) -> OrderInDB:
        db_order = Order(
            status=order.status,
            user_id=order.user_id,
            car_id=order.car_id,
            salesperson_id=order.salesperson_id,
            comments=order.comments
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return OrderInDB.from_orm(db_order)