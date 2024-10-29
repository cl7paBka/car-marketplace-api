from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.db.models import Car, TransmissionType, EngineType
from src.schemas.car import CarCreate, CarInDB, CarInfo
from typing import Optional, List


class CarRepository:
    """
        Repository for managing car-related database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_car(self, car: CarCreate) -> CarInDB:
        """
        Add a new car to the database and return the UserInDB model.

        Automatically handles created_at and updated_at using SQLAlchemy's server-side default values. You can choose
        specific engine and transmission types like "gasoline", "electric", "diesel" and "manual", "automatic"

        Car's vin_number must be unique.
        """
        db_car = Car(
            price=car.price,
            brand=car.brand,
            model=car.model,
            year=car.year,
            color=car.color,
            mileage=car.mileage,
            transmission=car.transmission,  # Transmission should be passed correctly if provided
            engine=car.engine,  # Engine should be passed correctly if provided
            vin_number=car.vin_number
            # orders relationship will not be handled here since Order is not ready yet
        )
        self.db.add(db_car)
        self.db.commit()
        self.db.refresh(db_car)
        return CarInDB.from_orm(db_car)

    def get_car_by_id(self, car_id: int) -> Optional[CarInDB]:
        """
        Retrieve a car by their ID from the database.
        """
        try:
            db_car = self.db.query(Car).filter(Car.id == car_id).one()
            return CarInDB.from_orm(db_car)
        except NoResultFound:
            return None

    def get_car_by_vin_number(self, vin_number: str) -> Optional[CarInDB]:
        """
        Retrieve a car by their vin_number from the database.
        """
        try:
            db_car = self.db.query(Car).filter(Car.vin_number == vin_number).one()
            return CarInDB.from_orm(db_car)
        except NoResultFound:
            return None

    def get_all_cars(self) -> Optional[List[CarInDB]]:
        """
        Retrieve all cars from the database.

        Returns a list of UserInDB schemas.
        """
        db_cars = self.db.query(Car).all()
        all_cars = [CarInDB.from_orm(car) for car in db_cars]
        if not all_cars:  # Return None if all_cars is empty
            return None
        return all_cars

    def get_cars_by_engine(self, car_engine: EngineType) -> Optional[List[CarInDB]]:
        """
        Retrieve all cars from the database with a specific engine type (gasoline, electric, diesel).

        Returns a list of UserInDB schemas.
        """
        db_cars = self.db.query(Car).filter(Car.engine == car_engine).all()
        all_cars = [CarInDB.from_orm(car) for car in db_cars]
        if not all_cars:  # Return None if all_cars is empty
            return None
        return all_cars

    def get_cars_by_transmission(self, car_transmission: TransmissionType) -> Optional[List[CarInDB]]:
        """
        Retrieve all cars from the database with a specific transmission type (manual, automatic).

        Returns a list of UserInDB schemas.
        """
        db_cars = self.db.query(Car).filter(Car.transmission == car_transmission).all()
        all_cars = [CarInDB.from_orm(car) for car in db_cars]
        if not all_cars:  # Return None if all_cars is empty
            return None
        return all_cars

    def delete_car_by_id(self, car_id: int) -> Optional[int]:
        """
        Delete a user from the database by their ID.

        Returns the ID of the deleted user if successful, otherwise None.
        """
        car = self.db.query(Car).filter(Car.id == car_id).first()
        if car:
            self.db.delete(car)
            self.db.commit()
            return car_id
        return None

    def update_car_by_id(self, car_id: int, car_data: CarInfo) -> Optional[CarInDB]:
        """
        Partially update a car's information by their ID.

        Returns the updated UserInDB schema if the car is found and updated, otherwise None.
        """
        db_car = self.db.query(Car).filter(Car.id == car_id).first()

        if not db_car:
            return None

        # Update only the fields that were provided (non-default fields)
        for field, value in car_data.dict(exclude_unset=True).items():
            setattr(db_car, field, value)

        self.db.commit()
        self.db.refresh(db_car)
        return CarInDB.from_orm(db_car)
