from typing import Any, Dict, List

from sqlalchemy.exc import NoResultFound

from src.schemas.base_response import (
    BaseResponse,
    BaseStatusMessageResponse
)
from src.schemas.cars import (
    CarCreateSchema,
    CarUpdateSchema,
    CarSchema
)
from src.utils.enums import (
    EngineType,
    TransmissionType
)
from src.utils.exception_handler import (
    handle_exception,
    handle_exception_default_500
)
from src.utils.repository import AbstractRepository


# TODO: Repr, Notation, Comments, Tosi Bosi :D
class CarsService:
    def __init__(self, cars_repo: AbstractRepository):
        self.cars_repo = cars_repo

    async def add(self, car: CarCreateSchema) -> BaseResponse[CarSchema]:
        try:
            existing_car = await self.cars_repo.get_one(vin_number=car.vin_number)
        except Exception as e:
            handle_exception_default_500(e)

        if existing_car:
            handle_exception(
                status_code=409,
                custom_message=f"Car with vin_number: '{car.vin_number}' already exists.",
            )

        try:
            cars_dict = car.model_dump()
            created_car = await self.cars_repo.create_one(cars_dict)
            return BaseResponse[CarSchema](
                status="success",
                message="Car created.",
                data=created_car
            )
        except Exception as e:
            handle_exception_default_500(e)

    async def get_one_by_filter(self, **filter_by) -> BaseResponse[CarSchema]:
        try:
            car = await self.cars_repo.get_one(**filter_by)
            if car:
                return BaseResponse[CarSchema](
                    status="success",
                    message="Car found.",
                    data=car
                )

        except Exception as e:
            handle_exception_default_500(e)

        handle_exception(status_code=404, custom_message="Car not found.")

    async def get_many_by_filter(self, **filter_by: Dict[str, Any]) -> BaseResponse[List[CarSchema]]:
        try:
            cars_by_criteria = await self.cars_repo.get_many(**filter_by)
            if cars_by_criteria:
                return BaseResponse[List[CarSchema]](
                    status="success",
                    message=f"Cars found.",
                    data=cars_by_criteria
                )
            return BaseResponse[List[CarSchema]](
                status="error",
                message=f"No cars found.",
                data=cars_by_criteria
            )
        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)

    async def get_all(self) -> BaseResponse[List[CarSchema]]:
        try:
            all_cars = await self.cars_repo.get_all()
            if all_cars:
                return BaseResponse[List[CarSchema]](
                    status="success",
                    message=f"All cars found.",
                    data=all_cars
                )
            return BaseResponse[List[CarSchema]](  # If there are no cars, return empty all_cars
                status="error",
                message=f"No cars found.",
                data=all_cars
            )
        except Exception as e:
            # Catch unexpected error
            handle_exception_default_500(e)

    async def update_by_id(self, car_id: int, car: CarUpdateSchema):
        try:
            existing_car_by_id = await self.cars_repo.get_one(id=car.id)
        except Exception as e:
            handle_exception_default_500(e)

        if not existing_car_by_id:
            handle_exception(
                status_code=404,
                custom_message=f"Car with id: '{car_id}' does not exist.",
            )

        if car.vin_number:
            try:
                existing_car_by_vin = await self.cars_repo.get_one(vin_number=car.vin_number)
            except Exception as e:
                handle_exception_default_500()

            if existing_car_by_vin:  # If car with this new vin_number exists throw HTTPException
                handle_exception(
                    status_code=409,
                    custom_message=f"Car with vin_number: '{car.vin_number}' already exists.",
                )

        try:
            cars_dict = car.model_dump()
            updated_car = await self.cars_repo.edit_one(car_id, cars_dict)
            return BaseResponse[CarSchema](
                status="success",
                message="Car updated.",
                data=updated_car
            )

        except Exception as e:
            handle_exception_default_500(e)

    async def delete_by_id(self, car_id: int) -> BaseStatusMessageResponse:
        try:
            await self.cars_repo.delete_one(car_id)
            return BaseStatusMessageResponse(
                status="success",
                message=f"Car with id {car_id} deleted."
            )
        except NoResultFound:  # Catches if there is no car with this id
            handle_exception(
                status_code=404,
                custom_message=f"No car with id: '{car_id}' found."
            )
        except Exception as e:
            handle_exception_default_500(e)
