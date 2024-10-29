from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.order import OrderCreate, OrderInfo
from src.db import get_db
from src.db.models import Role
from src.db.repositories.order_repository import OrderRepository
from src.db.repositories.user_repository import UserRepository
from typing import Optional, Dict

orders_api_router = APIRouter(prefix="/orders")


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


# For exception where salesperson_id is not user's id with role manager while creating or updating order
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def check_for_order_existence(order_id: int, order_repo: OrderRepository):
    existing_order = order_repo.get_order_by_id(order_id)
    if existing_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {order_id} not found")
    return existing_order


@orders_api_router.post("/create", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, order_repo: OrderRepository = Depends(get_order_repository),
                       user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Create a new order and return the created order's information.

    Returns the created order data and a success message.

    salesperson_id should not be equal to user's id, and user's with id = salesperson_id role should be equal to manager
    """
    if order.user_id == order.salesperson_id:
        raise HTTPException(status_code=400, detail="Order not created, user_id shouldn't be equal to salesperson_id")

    user_role_by_user_id = user_repo.get_user_by_id(order.salesperson_id).role
    if user_role_by_user_id != "manager":
        raise HTTPException(status_code=400,
                            detail="Order not created, salesperson_id is not user's id with role manager")

    created_order = order_repo.create_order(order)

    if created_order is not None:
        return {
            "status": "success",
            "message": f"Order with ID {created_order.id} created successfully.",
            "data": created_order.dict()
        }
    raise HTTPException(status_code=400, detail="Order not created")


@orders_api_router.get("/{order_id}", response_model=Dict)
async def get_order_by_id(order_id: int, order_repo: OrderRepository = Depends(get_order_repository)) -> Dict:
    """
    Retrieve an order by their ID.

    Returns 404 if the order is not found.
    """
    order = order_repo.get_order_by_id(order_id)
    if order is not None:
        return {
            "status": "success",
            "message": f"Order with ID {order_id} found.",
            "data": order.dict()
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {order_id} not found")


@orders_api_router.get("/with_car_id/{car_id}", response_model=Dict)
async def get_orders_by_car_id(car_id: int, order_repo: OrderRepository = Depends(get_order_repository)) -> Dict:
    """
    Retrieve all orders from the database with a specific car_id.

    Returns a list of UserInDB schemas.
    """
    all_orders = order_repo.get_orders_by_car_id(car_id)
    if all_orders is not None:
        data = {order.id: order.dict() for order in all_orders}
        return {
            "status": "success",
            "message": "All orders retrieved successfully",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders with car_id {car_id} found")


@orders_api_router.get("/with_user_id/{user_id}", response_model=Dict)
async def get_orders_by_user_id(user_id: int, order_repo: OrderRepository = Depends(get_order_repository)) -> Dict:
    """
    Retrieve all orders from the database with a specific user_id.

    Returns a list of UserInDB schemas.
    """
    all_orders = order_repo.get_orders_by_user_id(user_id)
    if all_orders is not None:
        data = {order.id: order.dict() for order in all_orders}
        return {
            "status": "success",
            "message": "All orders retrieved successfully",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders with user_id {user_id} found")


@orders_api_router.get("/with_salesperson_id/{salesperson_id}", response_model=Dict)
async def get_orders_by_salesperson_id(salesperson_id: int,
                                       order_repo: OrderRepository = Depends(get_order_repository)) -> Dict:
    """
    Retrieve all orders from the database with a specific salesperson_id.

    Returns a list of UserInDB schemas.
    """
    all_orders = order_repo.get_orders_by_salesperson_id(salesperson_id)
    if all_orders is not None:
        data = {order.id: order.dict() for order in all_orders}
        return {
            "status": "success",
            "message": "All orders retrieved successfully",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No orders with salesperson_id {salesperson_id} found")


@orders_api_router.get("/", response_model=Dict)
async def get_all_orders(order_repo: OrderRepository = Depends(get_order_repository)) -> Dict:
    """
    Retrieve all orders from the database.

    Returns a success message with the order data if found, otherwise raises a 404 error.
    """
    all_orders = order_repo.get_all_orders()
    if all_orders is not None:
        data = {order.id: order.dict() for order in all_orders}
        return {
            "status": "success",
            "message": "All orders retrieved successfully.",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders found")


@orders_api_router.patch("/update/{order_id}", response_model=Dict)
async def update_order(order_id: int, order_data: OrderInfo,
                       order_repo: OrderRepository = Depends(get_order_repository),
                       user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Update order information by their ID.

    If the order is not found, return 404.

    salesperson_id should not be equal to user's id, and user's with id = salesperson_id role should be equal to manager
    """
    existing_order = await check_for_order_existence(order_id, order_repo)

    # Raise HTTPException if user with id == salesperson_id is not manager
    if order_data.salesperson_id is not None:
        user_by_salesperson_id_role = user_repo.get_user_by_id(order_data.salesperson_id).role
        if user_by_salesperson_id_role != "manager":
            raise HTTPException(status_code=400,
                                detail="Order not updated, salesperson_id is not user's id with role manager.")

    # Raise HTTPException if user_id and salesperson_id in order_data and user_id == salesperson_id
    if order_data.user_id is not None and order_data.user_id == order_data.salesperson_id:
        raise HTTPException(
            status_code=400,
            detail="Order not updated, user_id shouldn't be equal to salesperson_id."
        )

    # Raise HTTPException if salesperson_id in order_data and user_id in existing order equals to salesperson id in order_data or
    # if user_id in order_data and salesperson_id in existing_order equals to user_id in order_data
    if (order_data.salesperson_id is not None and existing_order.user_id == order_data.salesperson_id) or (
            order_data.user_id is not None and existing_order.salesperson_id == order_data.user_id):
        raise HTTPException(
            status_code=400,
            detail="Order not updated, user_id shouldn't be equal to salesperson_id."
        )

    updated_order = order_repo.update_order_by_id(order_id, order_data)
    if updated_order is not None:
        return {
            "status": "success",
            "message": f"Order with ID {order_id} updated successfully.",
            "data": updated_order.dict()
        }


@orders_api_router.delete("/delete/{order_id")
async def delete_order(order_id: int, order_repo: OrderRepository = Depends(get_order_repository)):
    """
    Delete an order by their ID.

    Returns the ID of the deleted order, or 404 if the order is not found.
    """

    await check_for_order_existence(order_id, order_repo)

    deleted_order_id = order_repo.delete_order_by_id(order_id)
    if deleted_order_id is not None:
        return {
            "status": "success",
            "message": f"Order with ID {deleted_order_id} deleted successfully."
        }
    raise HTTPException(status_code=400, detail=f"Order with ID {order_id} could not be deleted")
