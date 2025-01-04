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


