from db.connection import get_db
from schemas.car import CarCreate, CarInDB, CarInfo
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CarRepository:
    def add_car(self, car: CarCreate):
        query = """
        INSERT INTO cars 
        (type, brand, model, year, price, color) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        with get_db() as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(query, (car.type, car.brand, car.model, car.year, car.price, car.color))

                car_id = cursor.fetchone()[0]

                conn.commit()
                logging.info(f"The car with {car_id} added to cars successfully")
                return car_id
            except Exception as e:
                print(f"Error while adding creating car: {e}")
                conn.rollback()

    def get_car_by_id(self, car_id: int):
        query = """
        SELECT *
        FROM cars
        WHERE id = %s
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (car_id,))
                row = cursor.fetchone()
                if row:
                    column_names = [desc[0] for desc in cursor.description]

                    car_data = dict(zip(column_names, row))

                    car_data['car_id'] = car_data.pop('id')

                    return CarInDB(**car_data)
                else:
                    logging.info(f"Car with ID {car_id} not found.")
                    return None

            except Exception as e:
                print(f"Erorr while seeking for car with id: {car_id} in cars: {e}")

    def delete_car_by_id(self, car_id: int):
        query = """
        DELETE FROM cars
        WHERE id = %s
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (car_id,))
                conn.commit()
                return car_id
            except Exception as e:
                print(f"Error while deleting car with id: {car_id} in cars: {e}")
                conn.rollback()
                return None

    def update_car_by_id(self, car_id: int, car: CarInfo):
        query = """
        UPDATE cars SET 
        """
        fields_to_update = []
        values = []

        if car.price is not None:
            fields_to_update.append("price = %s")
            values.append(car.price)

        if car.color is not None:
            fields_to_update.append("age = %s")
            values.append(car.color)

        if car.year is not None:
            fields_to_update.append("year = %s")
            values.append(car.year)

        if car.type is not None:
            fields_to_update.append("type = %s")
            values.append(car.type)

        if car.brand is not None:
            fields_to_update.append("brand = %s")
            values.append(car.brand)

        if not fields_to_update:
            return

        query += ", ".join(fields_to_update)
        query += " WHERE user_id = ?"

        values.append(car_id)

        with get_db() as conn:
            cursor = conn.cursor()
