from src.utils.repository import AbstractRepository
from src.schemas.cars import CarCreateSchema, CarUpdateSchema, CarSchema


class CarsService:
    def __init__(self, cars_repo: AbstractRepository):
        self.cars_repo = cars_repo

    async def create_car(self, car: CarCreateSchema):
        cars_dict = car.model_dump()
        created_car = await self.cars_repo.create_one(cars_dict)
        return created_car

    async def get_by_car_id(self, id: int):
        pass

    async def get_all_cars(self):
        all_cars = await self.cars_repo.get_all()
        return all_cars

    # async def create(self, user: UserCreateSchema):
    #     users_dict = user.model_dump()
    #     created_user = await self.users_repo.create_one(users_dict)
    #     return created_user
    #
    # async def get_one_by_filter(self):
    #     pass
    #
    # async def get_many_by_role(self):
    #     pass
    #
    # async def get_all(self):
    #     all_users = await self.users_repo.get_all()
    #     return all_users
    #
    # async def update_by_id(self, user_id):
    #     pass
    #
    # async def delete_by_id(self):
    #     pass
