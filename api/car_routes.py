import asyncio
from fastapi import APIRouter, Depends, HTTPException
from db.repository import CarRepository
from schemas.car import CarInDB, CarCreate, CarInfo

cars_api_router = APIRouter()


def get_car_repository():
    return CarRepository


@cars_api_router.get("/cars")
async def get_all_cars(repo: CarRepository = Depends(get_car_repository())):
    all_cars = repo.get_all_cars()
    if all_cars:
        data = {car.car_id: car.dict() for car in all_cars}
        # for car in all_cars:
        #     data[car.car_id] = car.dict()
        return {
            "status": "Success",
            "message": "All cars extracted successfully",
            "data": data
        }
    raise HTTPException(status_code=404, detail=f"No cars found")


@cars_api_router.get("/cars/get/{car_id}")
async def get_car_by_id(car_id: int, repo: CarRepository = Depends(get_car_repository())):
    car = repo.get_car_by_id(car_id)
    if car:
        return {
            "status": "Success",
            "message": f"Car with id {car_id} found",
            "data": car
        }
    raise HTTPException(status_code=404, detail="User not found")


@cars_api_router.post("/cars/add")
async def add_car(car: CarCreate, repo: CarRepository = Depends(get_car_repository())):
    car_id = repo.add_car(car)
    if car_id:
        return {
            "status": "Success",
            "message": "Car added successfully",
            "data": {
                "car_id": car_id,
                **car.dict()
            }
        }
    raise HTTPException(status_code=404, detail=f"Car not added")


@cars_api_router.put("/cars/update/{car_id}")
async def update_car_by_id(car_id: int, car: CarInfo, repo: CarRepository = Depends(get_car_repository())):
    existing_car = repo.get_car_by_id(car_id)
    if not existing_car:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")
    repo.update_car_by_id(car_id, car)
    return {
        "status": "Success",
        "message": f"Car with id {car_id} updated successfully",
        "data": CarInDB(car_id=car_id, **car.dict())
    }


@cars_api_router.delete("/cars/delete/{car_id}")
async def delete_car_by_id(car_id: int, repo: CarRepository = Depends(get_car_repository())):
    existing_car = repo.get_car_by_id(car_id)
    if not existing_car:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")

    deleted_car_id = repo.delete_car_by_id(car_id)
    if deleted_car_id is not None:
        return {
            "status": "success",
            "message": f"Car with id {deleted_car_id} has been deleted successfully"
        }
    raise HTTPException(status_code=404, detail=f"Car with id {car_id} has not been deleted")
