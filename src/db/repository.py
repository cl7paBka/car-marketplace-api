from src.db.connection import get_db
from src.schemas.car import CarCreate, CarInDB, CarInfo
from src.schemas.user import UserCreate, UserInDB, UserInfo
from src.schemas.order import OrderCreate, OrderInDB, OrderInfo
import logging
from typing import List, Optional

# Configure logging for repository actions
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class UserRepository:
    """
    Repository for managing user-related database operations.
    """

    def create_user(self, user: UserCreate) -> Optional[int]:
        """
        Add a new user to the database.

        Returns the new user's ID if successful, otherwise returns None.
        """
        query = """
        INSERT INTO users (name, surname, nickname, email)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (user.name, user.surname, user.nickname, user.email))
                user_id = cursor.fetchone()[0]
                conn.commit()
                logging.info(f"User with ID {user_id} created successfully.")
                return user_id
            except Exception as e:
                logging.error(f"Error creating user: {e}")
                conn.rollback()
                return None

    def get_user_by_id(self, user_id: int) -> Optional[UserInDB]:
        """
        Retrieve a user by their ID from the database.

        Returns the user as a UserInDB model if found, otherwise None.
        """
        query = "SELECT * FROM users WHERE id = %s"
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                if row:
                    column_names = [desc[0] for desc in cursor.description]
                    user_data = dict(zip(column_names, row))
                    return UserInDB(**user_data)
                logging.info(f"User with ID {user_id} not found.")
                return None
            except Exception as e:
                logging.error(f"Error retrieving user with ID {user_id}: {e}")
                return None

    def update_user_by_id(self, user_id: int, user: UserInfo) -> None:
        """
        Update a user's information by their ID.

        Only updates fields that are provided.
        """
        query = "UPDATE users SET "
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
            # Nothing to update
            return

        query += ", ".join(fields_to_update)
        query += " WHERE id = %s"
        values.append(user_id)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def delete_user_by_id(self, user_id: int) -> Optional[int]:
        """
        Delete a user from the database by their ID.

        Returns the user ID if successfully deleted, otherwise None.
        """
        query = "DELETE FROM users WHERE id = %s"
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (user_id,))
                conn.commit()
                logging.info(f"User with ID {user_id} deleted successfully.")
                return user_id
            except Exception as e:
                logging.error(f"Error deleting user with ID {user_id}: {e}")
                conn.rollback()
                return None

    def get_all_users(self) -> List[OrderInDB]:
        """
        Retrieve all orders from the database.

        Returns a list of OrderInDB models.
        """

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


class CarRepository:
    """
    Repository for managing car-related database operations.
    """

    def add_car(self, car: CarCreate) -> Optional[int]:
        """
        Add a new car to the database.

        Returns the new car's ID if successful, otherwise returns None.
        """
        query = """
        INSERT INTO cars (type, brand, model, year, price, color)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (car.type, car.brand, car.model, car.year, car.price, car.color))
                car_id = cursor.fetchone()[0]
                conn.commit()
                logging.info(f"Car with ID {car_id} added successfully.")
                return car_id
            except Exception as e:
                logging.error(f"Error adding car: {e}")
                conn.rollback()
                return None

    def get_car_by_id(self, car_id: int) -> Optional[CarInDB]:
        """
        Retrieve a car by its ID from the database.

        Returns the car as a CarInDB model if found, otherwise None.
        """
        query = "SELECT * FROM cars WHERE id = %s"
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
                logging.info(f"Car with ID {car_id} not found.")
                return None
            except Exception as e:
                logging.error(f"Error retrieving car with ID {car_id}: {e}")
                return None

    def update_car_by_id(self, car_id: int, car: CarInfo) -> None:
        """
        Update a car's details by its ID.

        Only updates fields that are provided.
        """
        query = "UPDATE cars SET "
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
            # Nothing to update
            return

        query += ", ".join(fields_to_update)
        query += " WHERE id = %s"
        values.append(car_id)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def delete_car_by_id(self, car_id: int) -> Optional[int]:
        """
        Delete a car from the database by its ID.

        Returns the car ID if successfully deleted, otherwise None.
        """
        query = "DELETE FROM cars WHERE id = %s"
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (car_id,))
                conn.commit()
                logging.info(f"Car with ID {car_id} deleted successfully.")
                return car_id
            except Exception as e:
                logging.error(f"Error deleting car with ID {car_id}: {e}")
                conn.rollback()
                return None

    def get_all_cars(self) -> List[CarInDB]:
        """
        Retrieve all cars from the database.

        Returns a list of CarInDB models.
        """
        query = "SELECT id, type, brand, model, year, price, color FROM cars"
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
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


class OrderRepository:
    """Repository for managing order-related database operations."""

    def create_order(self, order: OrderCreate) -> Optional[int]:
        """
        Add a new order to the database.

        Returns the new order's ID if successful, otherwise returns None.
        """
        query = """
        INSERT INTO orders (user_id, car_id, order_date, status)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (order.user_id, order.car_id, order.order_date, order.status))
                order_id = cursor.fetchone()[0]
                conn.commit()
                logging.info(f"Order with ID {order_id} created successfully.")
                return order_id
            except Exception as e:
                logging.error(f"Error creating order: {e}")
                conn.rollback()
                return None

    def get_order_by_id(self, order_id: int) -> Optional[OrderInDB]:
        """
        Retrieve an order by its ID from the database.

        Returns the order as an OrderInDB model if found, otherwise returns None.
        """
        query = "SELECT * FROM orders WHERE id = %s"
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (order_id,))
                row = cursor.fetchone()
                if row:
                    column_names = [desc[0] for desc in cursor.description]
                    order_data = dict(zip(column_names, row))
                    return OrderInDB(**order_data)
                logging.info(f"Order with ID {order_id} not found.")
                return None
            except Exception as e:
                logging.error(f"Error retrieving order with ID {order_id}: {e}")
                return None

    def update_order_by_id(self, order_id: int, order: OrderInfo) -> None:
        """
        Update an order's details by its ID.

        Only updates fields that are provided.
        """
        query = "UPDATE orders SET "
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
            # Nothing to update
            return

        query += ", ".join(fields_to_update)
        query += " WHERE id = %s"
        values.append(order_id)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def delete_order_by_id(self, order_id: int) -> Optional[int]:
        """
        Delete an order from the database by its ID.

        Returns the order ID if successfully deleted, otherwise None.
        """
        query = "DELETE FROM orders WHERE id = %s"
        with get_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (order_id,))
                conn.commit()
                logging.info(f"Order with ID {order_id} deleted successfully.")
                return order_id
            except Exception as e:
                logging.error(f"Error deleting order with ID {order_id}: {e}")
                conn.rollback()
                return None

    def get_all_orders(self) -> List[OrderInDB]:
        """
        Retrieve all orders from the database.

        Returns a list of OrderInDB models.
        """
        query = "SELECT id, user_id, car_id, order_date, status FROM orders"
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [
                OrderInDB(
                    id=row[0],
                    user_id=row[1],
                    car_id=row[2],
                    order_date=row[3],
                    status=row[4]
                )
                for row in rows
            ]
