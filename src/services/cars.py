from src.utils.repository import AbstractRepository
from src.schemas.cars import CarCreate, CarUpdate


class CarsService:
    def __init__(self, cars_repo: AbstractRepository):
        self.cars_repo = cars_repo

    async def create_car(self, car: CarCreate):
        cars_dict = car.model_dump()
        created_car = await self.cars_repo.create_one(cars_dict)
        return created_car

    async def get_all_cars(self):
        all_cars = await self.cars_repo.get_all()
        return all_cars