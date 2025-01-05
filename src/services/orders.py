from typing import Any, Dict, List

from sqlalchemy.exc import NoResultFound

from src.schemas.base_response import (
    BaseResponse,
    BaseStatusMessageResponse
)
from src.schemas.orders import (
    OrderCreateSchema,
    OrderSchema,
    OrderUpdateSchema
)
from src.utils.exception_handler import (
    handle_exception,
    handle_exception_default_500
)
from src.utils.repository import AbstractRepository
from src.utils.enums import Role


# TODO REPR, NOTATION, COMMENTS
class OrdersService:
    def __init__(
            self,
            orders_repo: AbstractRepository,
            users_repo: AbstractRepository,
            cars_repo: AbstractRepository
    ):
        self.orders_repo = orders_repo
        self.users_repo = users_repo
        self.cars_repo = cars_repo

    async def create(self, order: OrderCreateSchema) -> BaseResponse[OrderSchema]:
        try:
            existing_customer = await self.users_repo.get_one(id=order.user_id)
            existing_salesperson = await self.users_repo.get_one(id=order.salesperson_id)
            existing_car = await self.cars_repo.get_one(id=order.car_id)
        except Exception as e:
            handle_exception(
                status_code=500,
                custom_message=f"An unexpected error occurred while finding customer, salesperson and car by their id."
            )

        # All the necessary checks to create an order:
        # 1. Check: does the customer exist?
        if not existing_customer:
            return handle_exception(
                status_code=404,
                custom_message=f"Customer with ID: '{order.user_id}' was not found."
            )

        # 2. Check: is the customer's role set to 'customer'?
        if existing_customer.role.value != "customer":
            return handle_exception(
                status_code=400,
                custom_message=f"The user with ID: '{order.user_id}' is a {existing_customer.role.value}, not a customer."
            )

        # 3. Check: does the salesperson exist?
        if not existing_salesperson:
            return handle_exception(
                status_code=404,
                custom_message=f"Salesperson with ID: '{order.salesperson_id}' was not found."
            )

        # 4. Check: is the salesperson's role set to 'manager'?
        if existing_salesperson.role.value != "manager":
            return handle_exception(
                status_code=400,
                custom_message=f"The user with ID: '{order.salesperson_id}' is a {existing_salesperson.role.value},"
                               f" not a manager."
            )

        # 5. Check: does the car exist?
        if not existing_car:
            return handle_exception(
                status_code=404,
                custom_message=f"Car with ID: '{order.car_id}' was not found."
            )

        try:
            orders_dict = order.model_dump()
            created_order = await self.orders_repo.create_one(orders_dict)
            return BaseResponse[OrderSchema](
                status="success",
                message="Order created.",
                data=created_order
            )
        except Exception as e:
            handle_exception_default_500(e)