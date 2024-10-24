from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.car import CarCreate, CarInfo, CarInDB
from src.db import get_db
from src.db.models import TransmissionType, EngineType
from src.db.repositories.car_repository import CarRepository
from typing import Optional, Dict

cars_api_router = APIRouter(prefix="/cars")


# Dependency to get DB session
def get_car_repository(db: Session = Depends(get_db)) -> CarRepository:
    return CarRepository(db)


async def check_for_car_existence(car_id, car_repo: CarRepository):
    existing_car = car_repo.get_car_by_id(car_id)
    if existing_car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with ID {car_id} not found")


@cars_api_router.post("/create", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_car(car: CarCreate, car_repo: CarRepository = Depends(get_car_repository)) -> Dict:
    """
    Create a new car and return the created car's information.

    Returns the created car data and a success message.

    You can choose specific engine and transmission types like "gasoline", "electric", "diesel" and "manual",
    "automatic".

    Car's vin_number must be unique.
    """
    created_car = car_repo.create_car(car)
    if created_car is not None:
        return {
            "status": "success",
            "message": f"Car with ID {created_car.id} created successfully.",
            "data": created_car.dict()
        }
    raise HTTPException(status_code=400, detail=f"Car not created")


@cars_api_router.get("/{car_id}", response_model=Dict)
async def get_car_by_id(car_id: int, repo: CarRepository = Depends(get_car_repository)) -> Dict:
    """
    Retrieve a car by their ID.

    Returns the car data if found, otherwise raises a 404 error.
    """
    car = repo.get_car_by_id(car_id)
    if car is not None:
        return {
            "status": "success",
            "message": f"Car with ID {car_id} found.",
            "data": car.dict()
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with ID {car_id} not found")


@cars_api_router.get("/vin_number/{vin_number}", response_model=Dict)
async def get_car_by_vin_number(vin_number: str, car_repo: CarRepository = Depends(get_car_repository)) -> Dict:
    """
    Retrieve a car by their vin_number.

    Returns 404 if the car is not found.
    """
    car = car_repo.get_car_by_vin_number(vin_number)
    if car is not None:
        return {
            "status": "success",
            "message": f"Car with vin_number {vin_number} found, its ID is {car.id}",
            "data": car.dict()
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with vin_number {vin_number} not found")


@cars_api_router.get("/", response_model=Dict)
async def get_all_cars(car_repo: CarRepository = Depends(get_car_repository)):
    """
    Retrieve all cars from the repositories.

    Returns a success message with the car data if found, otherwise raises a 404 error.
    """
    all_cars = car_repo.get_all_cars()
    if all_cars is not None:
        data = {car.id: car.dict() for car in all_cars}
        return {
            "status": "success",
            "message": "All cars retrieved successfully",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No cars found")


@cars_api_router.get("/transmission/{transmission}", response_model=Dict)
async def get_cars_by_transmission(car_transmission: TransmissionType,
                                   car_repo: CarRepository = Depends(get_car_repository)) -> Dict:
    """
    Retrieve all cars with a specific transmission type (manual, automatic).
    """
    all_cars_with_specific_transmission = car_repo.get_cars_by_transmission(car_transmission)
    if all_cars_with_specific_transmission is not None:
        data = {car.id: car.dict() for car in all_cars_with_specific_transmission}
        return {
            "status": "success",
            "message": f"All cars with transmission type {car_transmission.value} retrieved successfully",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No cars with transmission type {car_transmission.value} found")


@cars_api_router.get("/engine/{engine}", response_model=Dict)
async def get_cars_by_engine(car_engine: EngineType,
                             car_repo: CarRepository = Depends(get_car_repository)) -> Dict:
    """
    Retrieve all cars with a specific engine type (gasoline, electric, diesel).
    """
    all_cars_with_specific_engine = car_repo.get_cars_by_engine(car_engine)
    if all_cars_with_specific_engine is not None:
        data = {car.id: car.dict() for car in all_cars_with_specific_engine}
        return {
            "status": "success",
            "message": f"All cars with transmission type {car_engine.value} retrieved successfully",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No cars with transmission type {car_engine.value} found")


@cars_api_router.patch("/update/{car_id}", response_model=Dict)
async def update_car(car_id: int, car_data: CarInfo,
                     car_repo: CarRepository = Depends(get_car_repository)) -> Dict:
    """
    Update an existing car's information by their ID.

    Returns the updated car data if the car is found, otherwise raises a 404 error.
    """
    await check_for_car_existence(car_id, car_repo)

    updated_car = car_repo.update_car_by_id(car_id, car_data)
    if updated_car is not None:
        return {
            "status": "success",
            "message": f"Car with id {car_id} updated successfully.",
            "data": updated_car.dict()
        }
    raise HTTPException(status_code=400, detail=f"Car with ID {car_id} could not be updated")


@cars_api_router.delete("/delete/{car_id}", response_model=Optional[Dict])
async def delete_car(car_id: int, car_repo: CarRepository = Depends(get_car_repository)) -> Optional[Dict]:
    """
    Delete a car by their ID.

    Returns the ID of the deleted car, or 404 if the car is not found.
    """
    await check_for_car_existence(car_id, car_repo)

    deleted_car_id = car_repo.delete_car_by_id(car_id)
    if deleted_car_id is not None:
        return {
            "status": "success",
            "message": f"Car with ID {deleted_car_id} deleted successfully."
        }
    raise HTTPException(status_code=400, detail=f"Car with ID {car_id} could not be deleted")
