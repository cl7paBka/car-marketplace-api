from db.connection import get_db
from schemas.car import CarCreate, CarInDB, CarInfo
from schemas.user import UserCreate, UserInfo, UserInDB
from schemas.order import OrderInfo, OrderCreate, OrderInDB
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
                logging.info(f"The car with id {car_id} added to cars successfully")
                return car_id
            except Exception as e:
                logging.info(f"Error occurred while creating car: {e}")
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
                    logging.info(f"Car with id {car_id} not found.")
                    return None

            except Exception as e:
                logging.info(f"Erorr while seeking for car with id: {car_id} in cars: {e}")

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
                logging.info(f"Error while deleting car with id {car_id} in cars: {e}")
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
            fields_to_update.append("color = %s")
            values.append(car.color)

        if car.year is not None:
            fields_to_update.append("year = %s")
            values.append(car.year)

        if car.type is not None:
            fields_to_update.append("type = %s")
            values.append(car.type)

        if car.model is not None:
            fields_to_update.append("model = %s")
            values.append(car.model)

        if car.brand is not None:
            fields_to_update.append("brand = %s")
            values.append(car.brand)

        if not fields_to_update:
            return

        query += ", ".join(fields_to_update)
        query += " WHERE id = %s"

        values.append(car_id)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def get_all_cars(self):
        query = """
        SELECT id, type, brand, model, year, price, color
        FROM cars
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            all_cars = [
                CarInDB(
                    car_id=row[0],
                    type=row[1],
                    brand=row[2],
                    model=row[3],
                    year=row[4],
                    price=row[5],
                    color=row[6]
                )
                for row in rows
            ]
            return all_cars


class UserRepository:
    def create_user(self, user: UserCreate):
        query = """
        INSERT INTO users
        (name, surname, nickname, email) VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        with get_db() as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(query, (user.name, user.surname, user.nickname, user.email))
                user_id = cursor.fetchone()[0]
                conn.commit()
                logging.info(f"The user with id {user_id} has been successfully created")
                return user_id
            except Exception as e:
                logging.info(f"Error occured while creating user: {e}")
                conn.rollback()

    def get_user_by_id(self, user_id: int):
        query = """
        SELECT *
        FROM users
        WHERE id = %s
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                if row:
                    column_names = [desc[0] for desc in cursor.description]

                    user_data = dict(zip(column_names, row))

                    return UserInDB(**user_data)
                else:
                    logging.info(f"User with id {user_id} not found")
                    return None
            except Exception as e:
                logging.info(f"Erorr while seeking for user with id: {user_id} in users: {e}")

    def get_all_users(self):
        query = """
        SELECT id, name, surname, nickname, email
        FROM users
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            all_users = [
                UserInDB(
                    id=row[0],
                    name=row[1],
                    surname=row[2],
                    nickname=row[3],
                    email=row[4]
                )
                for row in rows
            ]
            return all_users

    def update_user_by_id(self, user_id: int, user: UserInfo):
        query = """
        UPDATE users SET
        """
        fields_to_update = []
        values = []
        if user.name is not None:
            fields_to_update.append("name = %s")
            values.append(user.name)

        if user.surname is not None:
            fields_to_update.append("surname = %s")
            values.append(user.surname)

        if user.nickname is not None:
            fields_to_update.append("nickname = %s")
            values.append(user.nickname)

        if user.email is not None:
            fields_to_update.append("email = %s")
            values.append(user.email)

        if not fields_to_update:
            return

        query += ", ".join(fields_to_update)
        query += " WHERE id = %s"

        values.append(user_id)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def delete_user_by_id(self, user_id: int):
        query = """
        DELETE FROM users
        WHERE id = %s
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (user_id,))
                conn.commit()
                return user_id
            except Exception as e:
                logging.info(f"Error while deleting user with id: {user_id} in cars: {e}")
                conn.rollback()
                return None


class OrderRepository:
    def create_order(self, order: OrderCreate):
        query = """
        INSERT INTO orders
        (user_id, car_id, order_date, status) VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (order.user_id, order.car_id, order.order_date, order.status))
                order_id = cursor.fetchone()[0]
                conn.commit()
                logging.info(f"The order with id {order_id} has been successfully created")
                return order_id
            except Exception as e:
                logging.info(f"Error occurred while creating order: {e}")
                conn.rollback()

    def get_order_by_id(self, order_id: int):
        query = """
        SELECT *
        FROM orders
        WHERE id = %s
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (order_id,))
                row = cursor.fetchone()
                if row:
                    column_names = [desc[0] for desc in cursor.description]
                    order_data = dict(zip(column_names, row))
                    return OrderInDB(**order_data)
                else:
                    logging.info(f"Order with id {order_id} not found.")
                    return None
            except Exception as e:
                logging.info(f"Error while seeking for order with id: {order_id}")

    def get_all_orders(self):
        query = """
        SELECT id, user_id, car_id, order_date, status
        FROM orders
        """
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            all_orders = [
                OrderInDB(
                    id=row[0],
                    user_id=row[1],
                    car_id=row[2],
                    order_date=row[3],
                    status=row[4]
                )
                for row in rows
            ]
            return all_orders

    def delete_order_by_id(self, order_id: int):
        query = """
        DELETE FROM orders
        WHERE id = %s
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (order_id, ))
                conn.commit()
                return order_id
            except Exception as e:
                logging.info(f"Error while deleting order with id {order_id} in orders: {e}")
                conn.rollback()
                return None

    def update_order_by_id(self, order_id: int, order: OrderInfo):
        query = """
        UPDATE orders SET
        """
        fields_to_update = []
        values = []

        if order.user_id is not None:
            fields_to_update.append("user_id = %s")
            values.append(order.user_id)

        if order.car_id is not None:
            fields_to_update.append("car_id = %s")
            values.append(order.car_id)

        if order.order_date is not None:
            fields_to_update.append("order_date = %s")
            values.append(order.order_date)

        if order.status is not None:
            fields_to_update.append("status = %s")
            values.append(order.status)

        if not fields_to_update:
            return

        query += ", ".join(fields_to_update)
        query += " WHERE id = %s"

        values.append(order_id)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
