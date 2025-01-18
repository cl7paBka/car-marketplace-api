from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.api.dependencies import orders_service
from src.api.responses.orders_responses import (
    create_order_responses,
    get_order_by_id_responses,
    get_orders_by_status_responses,
    get_orders_by_customer_id_responses,
    get_orders_by_salesperson_id_responses,
    get_orders_by_car_id_responses,
    get_all_orders_responses,
    update_order_responses,
    delete_order_responses
)
from src.schemas.orders import OrderCreateSchema, OrderUpdateSchema, OrderSchema
from src.schemas.base_response import BaseResponse, BaseStatusMessageResponse
from src.services.orders import OrdersService
from src.utils.enums import OrderStatus
from src.utils.exception_handler import validate_payload  # Validates input data in api layer for patch end-point

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    path="/create",
    response_model=BaseResponse[OrderSchema],
    summary="Create a new order",
    description="""
    Create a new order by validating:
    - The existence of the customer (`user_id`) and confirming their role is 'customer'.
    - The existence of the salesperson (`salesperson_id`) and confirming their role is 'manager'.
    - The existence of the car (`car_id`).

    If all checks pass, the service will create a new order record.
    """,
    responses=create_order_responses
)
async def create_order(
        order: OrderCreateSchema,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to create a new order.
    """
    return await service.create(order)


@router.get(
    path="/{order_id}",
    response_model=BaseResponse[OrderSchema],
    summary="Get order by ID",
    description="""
    Retrieve a single order by its unique ID.
    
    Returns 404 if the order does not exist.
    """,
    responses=get_order_by_id_responses
)
async def get_order_by_id(
        order_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to fetch an order by its ID.
    """
    return await service.get_by_order_id(order_id)


@router.get(
    path="/status/{status}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by status",
    description="""
    Fetch all orders that match the specified status.
    
    Possible statuses: 'pending', 'completed' and 'canceled'.
    """,
    responses=get_orders_by_status_responses
)
async def get_orders_by_status(
        status: OrderStatus,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to retrieve orders filtered by a specific status.
    """
    return await service.get_by_status(status)


@router.get(
    path="/customer_id/{customer_id}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by customer's ID",
    description="""
    Fetch all orders associated with a specific customer ID.
    
    - Validates the user's role is 'customer'.
    - Returns 404 if the user does not exist, 400 if role mismatch.
    """,
    responses=get_orders_by_customer_id_responses
)
async def get_orders_by_customer_id(
        customer_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to retrieve orders belonging to a specific customer.
    """
    return await service.get_by_customer_id(customer_id)


@router.get(
    path="/salesperson_id/{salesperson_id}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by salesperson's ID",
    description="""
    Fetch all orders associated with a specific salesperson ID.
    
    - Validates the user's role is 'manager'.
    - Returns 404 if the user does not exist, 400 if role mismatch.
    """,
    responses=get_orders_by_salesperson_id_responses
)
async def get_orders_by_salesperson_id(
        salesperson_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to retrieve orders for a specific salesperson.
    """
    return await service.get_by_salesperson_id(salesperson_id)


@router.get(
    path="/car_id/{car_id}",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get orders by car's ID",
    description="""
    Fetch all orders tied to a particular car ID.
    
    Returns 404 if the car does not exist.
    """,
    responses=get_orders_by_car_id_responses
)
async def get_orders_by_car_id(
        car_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to retrieve orders referencing a specific car.
    """
    return await service.get_by_car_id(car_id)


@router.get(
    path="/",
    response_model=BaseResponse[List[OrderSchema]],
    summary="Get all orders",
    description="""
    Fetch all orders in the system.
    """,
    responses=get_all_orders_responses
)
async def get_all_orders(service: Annotated[OrdersService, Depends(orders_service)]):
    """
    Endpoint to retrieve all existing orders.
    """
    return await service.get_all()


@router.patch(
    path="/patch/{order_id}",
    response_model=BaseResponse[OrderSchema],
    summary="Update order details",
    description="""
    Update details of an existing order by its ID.
    
    - Checks for updated user_id, salesperson_id, or car_id, and validates existence/roles.
    - Returns 404 if the order or related entities don't exist, or 400 if role mismatch and 400 if payload is empty.
    """,
    responses=update_order_responses
)
async def update_order_by_order_id(
        order_id: int,
        new_order: OrderUpdateSchema,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to partially update an order.
    """
    validate_payload(new_order) # If new_order schema is just {}, throws 400
    return await service.update_by_id(order_id, new_order)


@router.delete(
    path="/delete/{order_id}",
    response_model=BaseStatusMessageResponse,
    summary="Delete an order",
    description="""
    Delete an order by its ID.

    Returns 404 if no such order is found.
    """,
    responses=delete_order_responses
)
async def delete_order_by_order_id(
        order_id: int,
        service: Annotated[OrdersService, Depends(orders_service)]
):
    """
    Endpoint to remove an existing order by its ID.
    """
    return await service.delete_by_id(order_id)
