from typing import Any, Dict, List

from sqlalchemy.exc import NoResultFound

from src.schemas.base_response import BaseResponse, BaseStatusMessageResponse
from src.schemas.orders import OrderCreateSchema, OrderSchema, OrderUpdateSchema
from src.utils.exception_handler import handle_exception, handle_exception_default_500
from src.utils.repository import AbstractRepository
from src.utils.enums import OrderStatus


class OrdersService:
    """
    Service layer for managing orders.

    This class provides methods to handle order-related operations, such as
    creating, retrieving, updating, and deleting cars. It acts as a bridge
    between the repository layer and the application layer.
    """

    def __init__(
            self,
            orders_repo: AbstractRepository,
            users_repo: AbstractRepository,
            cars_repo: AbstractRepository
    ) -> None:
        """
        Initialize the OrdersService with repositories for orders, users, and cars.
        """
        self.orders_repo = orders_repo
        self.users_repo = users_repo
        self.cars_repo = cars_repo

    async def create(self, order: OrderCreateSchema) -> BaseResponse[OrderSchema]:
        """
        Create a new order after validating associated entities.

        This method:
        1. Verifies that the customer, salesperson, and car exist.
        2. Checks roles for customer ('customer') and salesperson ('manager').
        3. Creates the order if all validations pass.
        """
        try:
            # Validate the existence of related entities
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

        # Create the order if validations pass
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

    async def get_by_order_id(self, order_id: int) -> BaseResponse[OrderSchema]:
        """
        Retrieve a single order by its ID.
        """
        try:
            order = await self.orders_repo.get_one(id=order_id)
            if order:  # If order exists
                return BaseResponse[OrderSchema](
                    status="success",
                    message="Order found.",
                    data=order
                )
        except Exception as e:
            handle_exception_default_500(e)  # Catches unexpected errors

        # If order not found
        handle_exception(status_code=404, custom_message="Order not found.")

    # Helper method for other get_orders functions
    async def _get_many_by_filter(self, **filter_by: Dict[str, Any]) -> [List[OrderSchema]]:
        """
        Retrieve all orders by specified criteria.
        """
        try:
            orders_by_criteria = await self.orders_repo.get_many(**filter_by)
            return orders_by_criteria
        except Exception as e:
            handle_exception_default_500(e)

    async def get_by_status(self, status: OrderStatus) -> BaseResponse[List[OrderSchema]]:
        """
        Retrieve order by its status.
        """
        filter_by = {"status": status}
        orders_by_status = await self._get_many_by_filter(**filter_by)
        if orders_by_status:  # If orders_by_status is not empty
            return BaseResponse[List[OrderSchema]](
                status="success",
                message=f"Orders with status: '{status.value}' found.",
                data=orders_by_status
            )
        return BaseResponse[List[OrderSchema]](  # If orders_by_status is empty
            status="error",
            message=f"No orders with status: '{status.value}' found.",
            data=orders_by_status
        )

    async def get_by_customer_id(self, customer_id: int) -> BaseResponse[List[OrderSchema]]:
        """
        Retrieve order by customer ID.
        """
        # Check for user existence by customer_id
        try:
            existing_customer = await self.users_repo.get_one(id=customer_id)
        except Exception as e:
            handle_exception_default_500(e)

        if not existing_customer:  # If there is no user by this customer_id
            handle_exception(
                status_code=404,
                custom_message=f"Customer with ID: '{customer_id}' was not found."
            )

        if existing_customer.role.value != "customer":  # If user's role is not customer
            return handle_exception(
                status_code=400,
                custom_message=f"The user with ID: '{customer_id}' is a {existing_customer.role.value}, not a customer."
            )

        # Logic for retrieving orders_by_customer_id:
        filter_by = {"user_id": customer_id}
        try:
            orders_by_customer_id = await self._get_many_by_filter(**filter_by)
            if orders_by_customer_id:  # If there are orders by this customer_id
                return BaseResponse[List[OrderSchema]](
                    status="success",
                    message=f"Orders for customer with ID: '{customer_id}' found.",
                    data=orders_by_customer_id
                )
            return BaseResponse[List[OrderSchema]](
                status="error",
                message=f"No orders for customer with ID: '{customer_id}' found.",
                data=orders_by_customer_id
            )
        except Exception as e:
            handle_exception_default_500(e)

    async def get_by_salesperson_id(self, salesperson_id: int) -> BaseResponse[List[OrderSchema]]:
        """
        Retrieve order by salesperson ID.
        """
        try:
            existing_salesperson = await self.users_repo.get_one(id=salesperson_id)
        except Exception as e:
            handle_exception_default_500(e)

        # Check for salesperson existence
        if not existing_salesperson:
            return handle_exception(
                status_code=404,
                custom_message=f"Salesperson with ID: '{salesperson_id}' was not found."
            )
        if existing_salesperson.role.value != "manager":  # If user's role is not manager
            return handle_exception(
                status_code=400,
                custom_message=f"The user with ID: '{salesperson_id}' is a {existing_salesperson.role.value}, not a manager."
            )

        # Logic for retrieving orders_by_salesperson_id:
        filter_by = {"salesperson_id": salesperson_id}
        try:
            orders_by_salesperson_id = await self._get_many_by_filter(**filter_by)
            if orders_by_salesperson_id:
                return BaseResponse[List[OrderSchema]](
                    status="success",
                    message=f"Orders for salesperson with ID: '{salesperson_id}' found.",
                    data=orders_by_salesperson_id
                )
            return BaseResponse[List[OrderSchema]](
                status="error",
                message=f"No orders for salesperson with ID: '{salesperson_id}' found.",
                data=orders_by_salesperson_id
            )
        except Exception as e:
            handle_exception_default_500(e)

    async def get_by_car_id(self, car_id: int) -> BaseResponse[List[OrderSchema]]:
        """
        Retrieve order by car ID.
        """
        try:
            existing_car = await self.cars_repo.get_one(id=car_id)
        except Exception as e:
            handle_exception_default_500(e)

        # Check for car existence
        if not existing_car:
            return handle_exception(
                status_code=404,
                custom_message=f"Car with ID: '{car_id}' was not found."
            )

        # Logic for retrieving orders_by_car_id:
        filter_by = {"car_id": car_id}
        orders_by_car_id = await self._get_many_by_filter(**filter_by)
        if orders_by_car_id:
            return BaseResponse[List[OrderSchema]](
                status="success",
                message=f"Orders for car with ID: '{car_id}' found.",
                data=orders_by_car_id
            )
        return BaseResponse[List[OrderSchema]](
            status="error",
            message=f"No orders for car with ID: '{car_id}' found."
        )

    async def get_all(self) -> BaseResponse[List[OrderSchema]]:
        """
        Retrieve all orders in the system.
        """
        try:
            all_orders = await self.orders_repo.get_all()
            if all_orders:
                return BaseResponse[List[OrderSchema]](
                    status="success",
                    message=f"All orders found.",
                    data=all_orders
                )
            return BaseResponse[List[OrderSchema]](
                status="error",
                message=f"No orders found.",
                data=all_orders
            )
        except Exception as e:
            handle_exception_default_500(e)

    async def update_by_id(self, order_id: int, order: OrderUpdateSchema) -> BaseResponse[OrderSchema]:
        """
        Update an order by its ID.
        """
        try:
            existing_order_by_id = await self.orders_repo.get_one(id=order_id)
        except Exception as e:
            handle_exception_default_500(e)

        if not existing_order_by_id:
            handle_exception(
                status_code=404,
                custom_message=f"Order with id: '{order_id}' does not exist.",
            )

        # Check the existence of related entities (customer, salesman and car) only if necessary
        if order.user_id is not None:
            try:
                customer = await self.users_repo.get_one(id=order.user_id)
            except Exception as e:
                handle_exception_default_500(e)
            if not customer:
                handle_exception(
                    status_code=404,
                    custom_message=f"Customer with ID: '{order.user_id}' was not found."
                )
            if customer.role.value != "customer":
                handle_exception(
                    status_code=400,
                    custom_message=f"The user with ID: '{order.user_id}' is a {customer.role.value}, not a customer."
                )

        if order.salesperson_id is not None:
            try:
                salesperson = await self.users_repo.get_one(id=order.salesperson_id)
            except Exception as e:
                handle_exception_default_500(e)
            if not salesperson:
                handle_exception(
                    status_code=404,
                    custom_message=f"Salesperson with ID: '{order.salesperson_id}' was not found."
                )
            if salesperson.role.value != "manager":
                handle_exception(
                    status_code=400,
                    custom_message=f"The user with ID: '{order.salesperson_id}' is a {salesperson.role.value}, not a manager."
                )

        if order.car_id is not None:
            try:
                car = await self.cars_repo.get_one(id=order.car_id)
            except Exception as e:
                handle_exception_default_500(e)
            if not car:
                handle_exception(
                    status_code=404,
                    custom_message=f"Car with ID: '{order.car_id}' was not found."
                )

        # Then update order after all checks
        try:
            update_data = order.model_dump(exclude_unset=True)
            updated_order = await self.orders_repo.update_one(order_id, update_data)
            return BaseResponse[OrderSchema](
                status="success",
                message=f"Order with id: '{order_id}' successfully updated.",
                data=updated_order
            )
        except Exception as e:
            handle_exception_default_500(e)

    async def delete_by_id(self, order_id: int) -> BaseStatusMessageResponse:
        """
        Delete an order by its ID.
        """
        try:
            await self.orders_repo.delete_one(order_id)
            return BaseStatusMessageResponse(
                status="success",
                message=f"Order with id {order_id} deleted."
            )
        except NoResultFound:  # Catches if there is no order with provided id
            handle_exception(
                status_code=404,
                custom_message=f"No order with id: '{order_id} found."
            )
        except Exception as e:
            handle_exception_default_500(e)
