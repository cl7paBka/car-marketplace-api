from fastapi import APIRouter, Depends
from typing import Annotated
from src.schemas.orders import (
    OrderCreate,
    OrderUpdate)
from src.services.orders import OrdersService
from src.api.dependencies import orders_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/create")
async def create_order(
        order: OrderCreate,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    created_order_id = await service.create_order(order)
    return {
        "status": "success",
        "message": f"Created order with ID: {created_order_id}"
    }


@router.get("/")
async def get_all_orders(service: Annotated[OrdersService, Depends(orders_service)]):
    all_orders = await service.get_all_orders()
    return {
        "status": "success",
        "message": f"All orders retrieved",
        "data": all_orders
    }
