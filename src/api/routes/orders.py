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

# @router.get(
#     path="/{order_id}"
# )

# @router.get(
#     path="/status/{status}"
# )

# @router.get(
#     path="/customer_id/{customer_id}"
# )

# @router.get(
#     path="/salesperson_id/{salesperson_id}"
# )

# @router.get(
#     path="/car_id/{car_id}"
# )

# @router.get(
#     path="/"
# )

# @router.patch(
#     path="/patch/{order_id}"
# )

# @router.delete(
#     path="/delete/{order_id}"
# )
