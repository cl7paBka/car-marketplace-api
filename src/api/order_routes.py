from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.order import OrderCreate, OrderInfo
from src.db import get_db
from src.db.models import OrderStatus
from src.db.repositories.order_repository import OrderRepository
from typing import Optional, Dict

orders_api_router = APIRouter(prefix="/orders")


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


async def check_for_order_existance(order_id: int, order_repo: OrderRepository):
    pass


# TODO: order endpoints (new order_by_status and others) and universal check for existance function for every type of
#  entities and TESTS + DOCKER + DOCKER.COMPOSE!

@orders_api_router.post("/create")
async def create_order(order: OrderCreate, order_repo: OrderRepository = Depends(get_order_repository)):
    if order.user_id == order.salesperson_id:
        raise HTTPException(status_code=400, detail="Order not created, user_id shouldn't be equal to salesperson_id")
    # TODO: Raise errors, where salesperson_id is not user's id with role manager
    created_order = order_repo.create_order(order)

    if created_order is not None:
        return {
            "status": "success",
            "message": f"Order with ID {created_order.id} created successfully.",
            "data": created_order.dict()
        }
    raise HTTPException(status_code=400, detail="Order not created")


@orders_api_router.get("/{order_id}")
async def get_order_by_id(order_id: int, order_repo: OrderRepository = Depends(get_order_repository)):
    order = order_repo.get_order_by_id(order_id)
    if order is not None:
        return {
            "status": "success",
            "message": f"Order with ID {order_id} found.",
            "data": order.dict()
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {order_id} not found")


@orders_api_router.get("/")
async def get_all_orders(order_repo: OrderRepository = Depends(get_order_repository)):
    all_orders = order_repo.get_all_orders()
    if all_orders is not None:
        data = {order.id: order.dict() for order in all_orders}
        return {
            "status": "success",
            "message": "All orders retrieved successfully.",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No orders found")

@orders_api_router.patch("/update/{order_id}")
async def update_order(order_id: int, order_data: OrderInfo,
                       order_repo: OrderRepository = Depends(get_order_repository)):
    # TODO: Check for order existence

    updated_order = order_repo.update_order_by_id(order_id, order_data)
    if updated_order is not None:
        return {
            "status": "success",
            "message": f"Order with ID {order_id} updated successfully.",
            "data": updated_order.dict()
        }


@orders_api_router.delete("/delete/{order_id")
async def delete_order(order_id: int, order_repo: OrderRepository = Depends(get_order_repository)):
    # TODO: Check for order existence

    deleted_order_id = order_repo.delete_order_by_id(order_id)
    if deleted_order_id is not None:
        return {
            "status": "success",
            "message": f"Order with ID {deleted_order_id} deleted successfully."
        }
    raise HTTPException(status_code=400, detail=f"Order with ID {order_id} could not be deleted")
