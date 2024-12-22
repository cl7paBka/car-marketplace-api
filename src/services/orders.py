from src.utils.repository import AbstractRepository
from src.schemas.orders import OrderCreate, OrderUpdate

class OrdersService:
    def __init__(self, orders_repo: AbstractRepository):
        self.orders_repo = orders_repo

    async def create_order(self, order: OrderCreate):
        orders_dict = order.model_dump()
        created_order = await self.orders_repo.create_one(orders_dict)
        return created_order

    async def get_all_orders(self):
        all_orders = await self.orders_repo.get_all()
        return all_orders