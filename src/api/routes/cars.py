from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.api.dependencies import cars_service
from src.services.cars import CarsService
from src.api.responses.cars_responses import (
    add_car_responses,
    get_car_by_id_responses,
    get_car_by_vin_responses,
    get_cars_by_engine_responses,
    get_cars_by_transmission_responses,
    get_all_cars_responses,
    update_car_responses,
    delete_car_responses
)
from src.schemas.cars import CarCreateSchema, CarUpdateSchema, CarSchema
from src.schemas.base_response import BaseResponse, BaseStatusMessageResponse
from src.utils.enums import EngineType, TransmissionType
from src.utils.exception_handler import validate_payload  # Validates input data in api layer for patch end-point

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


@router.post(
    path="/add",
    response_model=BaseResponse[CarSchema],
    summary="Add a new car",
    description="""
    Create a new car in the system.
    
    - Checks if a car with the given VIN number already exists.
    - If it does, returns a 409 Conflict.
    - Otherwise, creates a new record in the database.
    
    Possible engine types might be: 'electric', 'gasoline', 'diesel';
    Possible transmission types might be: 'manual', 'automatic'.
    """,
    responses=add_car_responses
)
async def add_car(
        car: CarCreateSchema,
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to create a new car.
    """
    return await service.add(car)


@router.get(
    path="/{car_id}",
    response_model=BaseResponse[CarSchema],
    summary="Get car by ID",
    description="""
    Retrieve a single car by its unique ID.
    
    - Returns 404 if the car is not found.
    - Returns 500 if an unexpected error occurs.
    """,
    responses=get_car_by_id_responses
)
async def get_car_by_id(
        car_id: int,
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to get car details by car ID.
    """
    filter_by = {"id": car_id}
    return await service.get_one_by_filter(**filter_by)


@router.get(
    path="/vin/{vin_number}",
    response_model=BaseResponse[CarSchema],
    summary="Get car by vin_number",
    description="""
    Retrieve a single car using the VIN number.
    
    - Returns 404 if no car matches the specified VIN.
    - Returns 500 if an unexpected error occurs.
    """,
    responses=get_car_by_vin_responses
)
async def get_car_by_vin(
        vin_number: str,
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to get car details by its VIN number.
    """
    filter_by = {"vin_number": vin_number}
    return await service.get_one_by_filter(**filter_by)


@router.get(
    path="/engine/{engine_type}",
    response_model=BaseResponse[List[CarSchema]],
    summary="Get cars by engine type",
    description="""
    Retrieve multiple cars filtered by engine type.
    
    Possible engine types might be: 'electric', 'gasoline', 'diesel'.
    """,
    responses=get_cars_by_engine_responses
)
async def get_cars_by_engine(
        engine_type: EngineType,
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to get cars with a specific engine type.
    """
    filter_by = {"engine": engine_type}
    return await service.get_many_by_filter(**filter_by)


@router.get(
    path="/transmission/{transmission_type}",
    response_model=BaseResponse[List[CarSchema]],
    summary="Get cars by transmission type",
    description="""
    Retrieve multiple cars filtered by transmission type.
    
    Possible transmission types might be: 'automatic', 'manual'.
    """,
    responses=get_cars_by_transmission_responses
)
async def get_cars_by_transmission(
        transmission_type: TransmissionType,
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to get cars by a specific transmission type.
    """
    filter_by = {"transmission": transmission_type}
    return await service.get_many_by_filter(**filter_by)


@router.get(
    path="/",
    response_model=BaseResponse[List[CarSchema]],
    summary="Get all cars",
    description="""
    Retrieve all cars in the system.
    
    - Returns a list of all car records.
    - Returns 500 if an unexpected error occurs.
    """,
    responses=get_all_cars_responses
)
async def get_all_cars(
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to fetch a list of all available cars.
    """
    return await service.get_all()


@router.patch(
    path="/patch/{car_id}",
    response_model=BaseResponse[CarSchema],
    summary="Update car details",
    description="""
    Update an existing car's details by its unique ID.
    
    - Validates that the VIN (if changed) doesn't conflict.
    - Returns 404 if no car matches the provided ID.
    - Returns 500 if an unexpected error occurs.
    """,
    responses=update_car_responses
)
async def update_car_by_car_id(
        car_id: int,
        new_car: CarUpdateSchema,
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to update a car's information partially.
    """
    validate_payload(new_car)
    return await service.update_by_id(car_id, new_car)


@router.delete(
    path="/delete/{car_id}",
    response_model=BaseStatusMessageResponse,
    summary="Delete a car",
    description="""
    Delete a car by its ID.
    
    - Returns 404 if no car matches the provided ID.
    - Returns 500 if an unexpected error occurs.
    """,
    responses=delete_car_responses
)
async def delete_car_by_car_id(
        car_id: int,
        service: Annotated[CarsService, Depends(cars_service)]
):
    """
    Endpoint to delete a car by ID.
    """
    return await service.delete_by_id(car_id)
