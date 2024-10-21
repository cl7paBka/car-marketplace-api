from fastapi import APIRouter, Depends, HTTPException
from src.db.repository import OrderRepository
from src.schemas.order import OrderCreate, OrderInfo, OrderInDB
from typing import Dict

orders_api_router = APIRouter()


def get_order_repository():
    """Dependency to get the OrderRepository instance."""
    return OrderRepository


@orders_api_router.get("/orders/", response_model=Dict)
async def get_all_orders(repo: OrderRepository = Depends(get_order_repository())) -> Dict:
    """
    Retrieve all orders from the repository.

    Returns a success message with the order data if fount, otherwise raises a 404 error.
    """
    all_orders = repo.get_all_orders()
    if all_orders:
        data = {order.id: order.dict() for order in all_orders}
        return {
            "status": "success",
            "message": "All orders retrieved successfully.",
            "data": data
        }
    raise HTTPException(status_code=404, detail=f"No orders found")


@orders_api_router.get("/orders/get/{user_id}", response_model=Dict)
async def get_order_by_id(order_id: int, repo: OrderRepository = Depends(get_order_repository())) -> Dict:
    """
    Retrieve an order by their ID.

    Returns the order data if found, otherwise raises a 404 error.
    """
    order = repo.get_order_by_id(order_id)
    if order:
        return {
            "status": "Success",
            "message": f"Order with id {order_id} found",
            "data": order
        }
    raise HTTPException(status_code=404, detail="Order not found")


@orders_api_router.post("/orders/create", response_model=Dict)
async def create_order(order: OrderCreate, repo: OrderRepository = Depends(get_order_repository())) -> Dict:
    """
    Create a new order in the repository.

    Returns the created order data and a success message.
    """
    order_id = repo.create_order(order)
    if order_id:
        return {
            "status": "success",
            "message": "Order created successfully.",
            "data": {
                "order_id": order_id,
                **order.dict()
            }
        }
    raise HTTPException(status_code=404, detail=f"Order not created")


@orders_api_router.put("/orders/update/{order_id}", response_model=Dict)
async def update_order_by_id(order_id: int, order: OrderInfo,
                             repo: OrderRepository = Depends(get_order_repository())) -> Dict:
    """
    Update an existing order's information by their ID.

    Returns the updated order data if the order is found, otherwise raises a 404 error.
    """
    existing_order = repo.get_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

    repo.update_order_by_id(order_id, order)

    return {
        "status": "success",
        "message": f"Order with ID {order_id} updated successfully.",
        "data": OrderInDB(id=order_id, **order.dict())
    }


@orders_api_router.delete("/orders/delete/{order_id}", response_model=Dict)
async def delete_order_by_id(order_id: int, repo: OrderRepository = Depends(get_order_repository())) -> Dict:
    """
    Delete an order by their ID from the repository.

    Returns a success message if the order is deleted, otherwise raises a 404 error.
    """
    existing_order = repo.get_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

    deleted_order_id = repo.delete_order_by_id(order_id)
    if deleted_order_id is not None:
        return {
            "status": "success",
            "message": f"Order with ID {deleted_order_id} deleted successfully."
        }
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} has not been deleted")
