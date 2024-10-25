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

    def get_order_by_id(self, order_id: int) -> Optional[OrderInDB]:
        try:
            db_order = self.db.query(Order).filter(Order.id == order_id).one()
            return OrderInDB.from_orm(db_order)
        except NoResultFound:
            return None

    def get_orders_by_car_id(self):
        pass

    def get_orders_by_user_id(self):
        pass

    def get_orders_by_salesperson_id(self):
        pass

    def get_all_orders(self) -> Optional[List[OrderInDB]]:
        db_orders = self.db.query(Order)
        all_orders = [OrderInDB.from_orm(order) for order in db_orders]
        if len(all_orders) == 0:
            return None
        return all_orders

    def delete_order_by_id(self, order_id: int) -> Optional[int]:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            self.db.delete(order)
            self.db.commit()
            return order_id
        return None

    def update_order_by_id(self, order_id: int, order_data: OrderInfo) -> Optional[OrderInDB]:
        # TODO: Add raise errors in update_order_by_id end-point if salesperson_id == user_id or salesperson_id refers not to manager
        db_order = self.db.query(Order).filter(Order.id == order_id)

        if not db_order:
            return None

        for field, value in order_data.dict(exclude_unset=True).items():
            setattr(db_order, field, value)

        self.db.commit()
        self.db.refresh(db_order)
        return OrderInDB.from_orm(db_order)
