from src.utils.repository import AbstractRepository
from src.schemas.orders import OrderCreateSchema, OrderUpdateSchema


class OrdersService:
    def __init__(self, orders_repo: AbstractRepository):
        self.orders_repo = orders_repo

    async def create_order(self, order: OrderCreateSchema):
        orders_dict = order.model_dump()
        created_order = await self.orders_repo.create_one(orders_dict)
        return created_order

    async def get_all_orders(self):
        all_orders = await self.orders_repo.get_all()
        return all_orders


    # async def create(self, user: UserCreateSchema):
    #     users_dict = user.model_dump()
    #     created_user = await self.users_repo.create_one(users_dict)
    #     return created_user
    #
    # async def get_one_by_filter(self):
    #     pass
    #
    # async def get_many_by_role(self):
    #     pass
    #
    # async def get_all(self):
    #     all_users = await self.users_repo.get_all()
    #     return all_users
    #
    # async def update_by_id(self, user_id):
    #     pass
    #
    # async def delete_by_id(self):
    #     pass
