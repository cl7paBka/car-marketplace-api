from fastapi import APIRouter, Depends, HTTPException
from src.db.repository import CarRepository
from src.schemas.car import CarCreate, CarInfo, CarInDB
from typing import Dict

cars_api_router = APIRouter()


# Add annotation
def get_car_repository():
    """Dependency to get the CarRepository instance."""
    return CarRepository


@cars_api_router.get("/cars/", response_model=Dict)
async def get_all_cars(repo: CarRepository = Depends(get_car_repository())):
    """
    Retrieve all cars from the repository.

    Returns a success message with the car data if found, otherwise raises a 404 error.
    """
    all_cars = repo.get_all_cars()
    if all_cars:
        data = {car.car_id: car.dict() for car in all_cars}
        # for car in all_cars:
        #     data[car.car_id] = car.dict()
        return {
            "status": "success",
            "message": "All cars retrieved successfully",
            "data": data
        }
    raise HTTPException(status_code=404, detail=f"No cars found")


@cars_api_router.get("/cars/get/{car_id}", response_model=Dict)
async def get_car_by_id(car_id: int, repo: CarRepository = Depends(get_car_repository())) -> Dict:
    """
    Retrieve a car by their ID.

    Returns the car data if found, otherwise raises a 404 error.
    """
    car = repo.get_car_by_id(car_id)
    if car:
        return {
            "status": "success",
            "message": f"Car with ID {car_id} found.",
            "data": car
        }
    raise HTTPException(status_code=404, detail="Car not found")


@cars_api_router.post("/cars/add", response_model=Dict)
async def add_car(car: CarCreate, repo: CarRepository = Depends(get_car_repository())) -> Dict:
    """
    Add a new car into the repository.

    Returns the added car data and a success message.
    """
    car_id = repo.add_car(car)
    if car_id:
        return {
            "status": "success",
            "message": "Car added successfully.",
            "data": {
                "car_id": car_id,
                **car.dict()
            }
        }
    raise HTTPException(status_code=404, detail=f"Car not added")


@cars_api_router.put("/cars/update/{car_id}", response_model=Dict)
async def update_car_by_id(car_id: int, car: CarInfo,
                           repo: CarRepository = Depends(get_car_repository())) -> Dict:
    """
    Update an existing car's information by their ID.

    Returns the updated car data if the user is found, otherwise raises a 404 error.
    """
    existing_car = repo.get_car_by_id(car_id)
    if not existing_car:
        raise HTTPException(status_code=404, detail=f"Car with ID {car_id} not found")

    repo.update_car_by_id(car_id, car)

    return {
        "status": "success",
        "message": f"Car with ID {car_id} updated successfully.",
        "data": CarInDB(car_id=car_id, **car.dict())
    }


@cars_api_router.delete("/cars/delete/{car_id}", response_model=Dict)
async def delete_car_by_id(car_id: int, repo: CarRepository = Depends(get_car_repository())) -> Dict:
    """
    Delete a car by their ID from the repository.

    Returns a success message if the car is deleted, otherwise raises a 404 error
    """
    existing_car = repo.get_car_by_id(car_id)
    if not existing_car:
        raise HTTPException(status_code=404, detail=f"Car with ID {car_id} not found")

    deleted_car_id = repo.delete_car_by_id(car_id)
    if deleted_car_id is not None:
        return {
            "status": "success",
            "message": f"Car with id {deleted_car_id} deleted successfully"
        }
    raise HTTPException(status_code=404, detail=f"Car with ID {car_id} could not be deleted")
