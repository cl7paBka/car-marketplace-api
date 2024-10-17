import asyncio
from fastapi import APIRouter, Depends, HTTPException
from db.repository import CarRepository
from schemas.car import CarInDB, CarCreate, CarInfo

cars_api_router = APIRouter()


def get_car_repository():
    return CarRepository


@cars_api_router.get("/cars/get/{car_id}")
async def get_car_by_id(car_id: int, repo: CarRepository = Depends(get_car_repository())):
    car = repo.get_car_by_id(car_id)
    if car:
        return {
            "status": "success",
            "message": f"Car with id {car_id} found",
            "data": car
        }
    raise HTTPException(status_code=404, detail="User not found")


@cars_api_router.post("/cars/add")
async def add_car(car: CarCreate, repo: CarRepository = Depends(get_car_repository())):
    car_id = repo.add_car(car)
    if car_id:
        return {
            "status": "success",
            "message": "Car added successfully",
            "data": {
                "car_id": car_id,
                **car.dict()
            }
        }
    raise HTTPException(status_code=404, detail=f"Car not added with id {car_id}")


@cars_api_router.delete("/cars/delete/{car_id}")
async def delete_car_by_id(car_id: int, repo: CarRepository = Depends(get_car_repository())):
    deleted_car_id = repo.delete_car_by_id(car_id)
    if car_id is not None:
        return {
            "status": "success",
            "message": f"Car with id {deleted_car_id} deleted successfully"
        }
    raise HTTPException(status_code=404, detail=f"Car not deleted with id {car_id}")


@cars_api_router.put("/cars/update/{car_id}")
async def update_car_by_id(car_id: int, car: CarInfo, repo: CarRepository = Depends(get_car_repository())):
    pass


@cars_api_router.get("/cars")
async def get_all_cars():
    pass