from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.api.dependencies import cars_service
# from src.api.responses.cars_responses import (
#
# )
from src.schemas.cars import (
    CarCreateSchema,
    CarUpdateSchema,
    CarSchema
)
from src.schemas.base_response import (
    BaseResponse,
    BaseStatusMessageResponse
)
from src.services.cars import CarsService
from src.utils.enums import (
    EngineType,
    TransmissionType
)

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


# TODO: all descriptions and responses for end-points
@router.post(
    path="/add",
    response_model=BaseResponse[CarSchema],
    summary="Add a new car",
    description="""
    
    """
    # responses=
)
async def add_car(
        car: CarCreateSchema,
        service: Annotated[CarsService, Depends(cars_service)]
):
    return await service.add(car)


@router.get(
    path="/{car_id}",
    response_model=BaseResponse[CarSchema],
    summary="Get car by ID",
    description="""
    
    """
    # responses=
)
async def get_car_by_id(
        car_id: int,
        service: Annotated[CarsService, Depends(cars_service)]
):
    filter_by = {"id": car_id}
    return await service.get_one_by_filter(**filter_by)


@router.get(
    path="/vin/{vin_number}",
    response_model=BaseResponse[CarSchema],
    summary="Get car by vin_number",
    description="""
    """
    # responses=
)
async def get_car_by_vin(
        vin_number: str,
        service: Annotated[CarsService, Depends(cars_service)]
):
    filter_by = {"vin_number": vin_number}
    return await service.get_one_by_filter(**filter_by)


@router.get(
    path="/engine/{engine_type}",
    response_model=BaseResponse[List[CarSchema]],
    summary="Get cars by engine type",
    description="""
        
    """
    # responses
)
async def get_cars_by_engine(
        engine_type: EngineType,
        service: Annotated[CarsService, Depends(cars_service)]
):
    filter_by = {"engine": engine_type}
    return await service.get_many_by_filter(**filter_by)


@router.get(
    path="/transmission/{transmission_type}",
    response_model=BaseResponse[List[CarSchema]],
    summary="Get cars by transmission type",
    description="""
    
    """,
    # responses
)
async def get_cars_by_transmission(
        transmission_type: TransmissionType,
        service: Annotated[CarsService, Depends(cars_service)]
):
    filter_by = {"transmission": transmission_type}
    return await service.get_many_by_filter(**filter_by)


@router.get(
    path="/",
    response_model=BaseResponse[List[CarSchema]],
    summary="Get all cars",
    description="""
    """
    # responses=
)
async def get_all_cars(
        service: Annotated[CarsService, Depends(cars_service)]
):
    return await service.get_all()


@router.patch(
    path="/patch/{car_id}",
    response_model=BaseResponse[CarSchema],
    summary="Update car details",
    description="""
    """
    #     responses=
)
async def update_car_by_car_id(
        car_id: int,
        new_car: CarUpdateSchema,
        service: Annotated[CarsService, Depends(cars_service)]
):
    return await service.update_by_id(car_id, new_car)


@router.delete(
    path="/delete/{car_id}",
    response_model=BaseStatusMessageResponse,
    summary="Delete a car",
    description="""
    """
    # responses=
)
async def delete_car_by_car_id(
        car_id: int,
        service: Annotated[CarsService, Depends(cars_service)]
):
    return await service.delete_by_id(car_id)