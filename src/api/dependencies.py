from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session

from src.repositories.users import UsersRepository
from src.services.users import UsersService

from src.repositories.cars import CarsRepository
from src.services.cars import CarsService

from src.repositories.orders import OrdersRepository
from src.services.orders import OrdersService


def users_service(session: AsyncSession = Depends(get_async_session)) -> UsersService:
    users_repository = UsersRepository(session=session)
    return UsersService(users_repository)


def cars_service(session: AsyncSession = Depends(get_async_session)) -> CarsService:
    cars_repository = CarsRepository(session=session)
    return CarsService(cars_repository)


def orders_service(session: AsyncSession = Depends(get_async_session)) -> OrdersService:
    orders_repository = OrdersRepository(session=session)
    return OrdersService(orders_repository)
