from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.api.dependencies import orders_service
# from src.api.responses.orders_responses import
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
