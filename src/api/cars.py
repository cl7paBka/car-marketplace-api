from fastapi import APIRouter, Depends
from typing import Annotated
from src.schemas.cars import (
    CarCreateSchema,
    CarUpdateSchema)
from src.services.cars import CarsService
from src.api.dependencies import cars_service

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


# @router.post("/create")
# async def create_car(
#         car: CarCreate,
#         service: Annotated[CarsService, Depends(cars_service)]
# ):
#     created_car_id = await service.create_car(car)
#     return {
#         "status": "success",
#         "message": f"Created user with ID: {created_car_id}"
#     }
#
# @router.get("/")
# async def get_all_cars(service: Annotated[CarsService, Depends(cars_service)]):
#     all_cars = await service.get_all_cars()
#     return {
#         "status": "success",
#         "message": f"All cars retrieved",
#         "data": all_cars
#     }