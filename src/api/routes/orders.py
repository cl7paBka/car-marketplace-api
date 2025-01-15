from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.api.dependencies import orders_service
# from src.api.responses.orders_responses import # TODO: responses for orders
from src.schemas.orders import (
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderSchema
)
from src.schemas.base_response import (
    BaseResponse,
    BaseStatusMessageResponse
)
from src.services.orders import OrdersService
from src.utils.enums import OrderStatus
from src.utils.exception_handler import validate_payload  # Validates input data in api layer for patch end-point

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# TODO: Make better end-points
@router.post(
    path="/create",
    response_model=BaseResponse[OrderSchema],
    summary="Create a new order",
    description="""
    """
    # responses
)
async def create_order(
        order: OrderCreateSchema,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.create(order)


@router.get(
    path="/{order_id}",
    response_model=BaseResponse[OrderSchema],
    summary="Get order by ID",
    description="""
    
    """,
    # responses
)
async def get_order_by_id(
        order_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.get_by_order_id(order_id)


@router.get(
    path="/status/{status}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by status",
    description="""
    
    """,
    # responses
)
async def get_orders_by_status(
        status: OrderStatus,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.get_by_status(status)


@router.get(
    path="/customer_id/{customer_id}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by customer's ID",
    description="""
    """,
    # responses
)
async def get_orders_by_customer_id(
        customer_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.get_by_customer_id(customer_id)


@router.get(
    path="/salesperson_id/{salesperson_id}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by salesperson's ID",
    description="""
    """
    # responses
)
async def get_orders_by_salesperson_id(
        salesperson_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.get_by_salesperson_id(salesperson_id)


@router.get(
    path="/car_id/{car_id}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by car's ID",
    description="""
    """,
    # responses
)
async def get_orders_by_car_id(
        car_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.get_by_car_id(car_id)


@router.get(
    path="/",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get all orders",
    description="""
    """
    # responses
)
async def get_all_orders(service: Annotated[OrdersService, Depends(orders_service)]):
    return await service.get_all()


@router.patch(
    path="/patch/{order_id}",
    response_model=BaseResponse[OrderSchema],
    summary="Update order details",
    description="""
    """
    # responses
)
async def update_order_by_order_id(
        order_id: int,
        new_order: OrderUpdateSchema,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.update_by_id(order_id, new_order)


@router.delete(
    path="/delete/{order_id}",
    response_model=BaseStatusMessageResponse,
    summary="Delete an order",
    description="""
    """
    # responses
)
async def delete_order_by_order_id(
        order_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    return await service.delete_by_id(order_id)
