from fastapi import APIRouter, Depends, HTTPException
from db.repository import OrderRepository
from schemas.order import OrderInfo, OrderCreate, OrderInDB

orders_api_router = APIRouter()


def get_order_repository():
    return OrderRepository


@orders_api_router.get("/orders")
async def get_all_orders(repo: OrderRepository = Depends(get_order_repository())):
    all_orders = repo.get_all_orders()
    if all_orders:
        data = {order.id: order.dict() for order in all_orders}
        return {
            "status": "Success",
            "message": "All orders extracted successfully",
            "data": data
        }
    raise HTTPException(status_code=404, detail=f"No orders found")


@orders_api_router.get("/orders/get/{user_id}")
async def get_order_by_id(order_id: int, repo: OrderRepository = Depends(get_order_repository())):
    order = repo.get_order_by_id(order_id)
    if order:
        return {
            "status": "Success",
            "message": f"Order with id {order_id} found",
            "data": order
        }
    raise HTTPException(status_code=404, detail="Order not found")


@orders_api_router.post("/orders/create")
async def create_order(order: OrderCreate, repo: OrderRepository = Depends(get_order_repository())):
    order_id = repo.create_order(order)
    if order_id:
        return {
            "status": "Success",
            "message": "Order created successfully",
            "data": {
                "order_id": order_id,
                **order.dict()
            }
        }
    raise HTTPException(status_code=404, detail=f"Order not created")


@orders_api_router.put("/orders/update/{order_id}")
async def update_order_by_id(order_id: int, order: OrderInfo, repo: OrderRepository = Depends(get_order_repository())):
    existing_order = repo.get_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    repo.update_order_by_id(order_id, order)
    return {
        "status": "Success",
        "message": f"Order with id {order_id} has been updated",
        "data": OrderInDB(id=order_id, **order.dict())
    }

@orders_api_router.delete("/orders/delete/{order_id}")
async def delete_order_by_id(order_id: int, repo: OrderRepository = Depends(get_order_repository())):
    existing_order = repo.get_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")

    deleted_order_id = repo.delete_order_by_id(order_id)
    if deleted_order_id is not None:
        return {
            "status": "success",
            "message": f"Order with id {deleted_order_id} has been successfully deleted"
        }
    raise HTTPException(status_code=404, detail=f"Order with id {order_id} has not been deleted")
