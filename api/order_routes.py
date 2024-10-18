from fastapi import APIRouter, Depends, HTTPException
from db.repository import OrderRepository
from schemas.order import OrderInfo, OrderCreate, OrderInDB

orders_api_router = APIRouter()


@orders_api_router.get("/orders")
async def get_all_orders():
    pass


@orders_api_router.get("/orders/get/{user_id}")
async def get_order_by_id():
    pass


@orders_api_router.post("/orders/create")
async def create_order():
    pass


@orders_api_router.put("/orders/update/{order_id}")
async def update_order_by_id(order_id: int):
    pass

@orders_api_router.delete("/orders/delete/{order_id}")
async def delete_order_by_id(order_id: int):
    pass
