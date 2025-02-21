from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from src.db.db import Base
from src.utils.enums import Role, OrderStatus, TransmissionType, EngineType
from src.schemas.users import UserSchema
from src.schemas.cars import CarSchema
from src.schemas.orders import OrderSchema


# Models
class Orders(Base):
    __tablename__ = "orders"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Order details
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                 nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), nullable=False,
                                                server_default=OrderStatus.pending.value)
    comments: Mapped[str] = mapped_column(String(255), nullable=False)

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    # TODO: Refactor user_id to customer_id
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)
    salesperson_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user: Mapped["Users"] = relationship("Users", back_populates="orders", foreign_keys=[user_id])
    car: Mapped["Cars"] = relationship("Cars", back_populates="orders")
    salesperson: Mapped["Users"] = relationship(
        "Users", foreign_keys=[salesperson_id], overlaps="sales_orders"
    )  # `overlaps` to resolve relationship uncertainty

    def to_read_model(self) -> OrderSchema:
        return OrderSchema(
            id=self.id,
            user_id=self.user_id,
            car_id=self.car_id,
            salesperson_id=self.salesperson_id,
            status=self.status,
            comments=self.comments,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


class Users(Base):
    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # User information
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(SAEnum(Role), nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                 nullable=False)

    # Relationships
    orders: Mapped[list["Orders"]] = relationship(
        "Orders", back_populates="user", foreign_keys="Orders.user_id"
    )
    sales_orders: Mapped[list["Orders"]] = relationship(
        "Orders", foreign_keys="Orders.salesperson_id"
    )

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            name=self.name,
            surname=self.surname,
            email=self.email,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


class Cars(Base):
    __tablename__ = "cars"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Car details
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # TODO: Ensure this value is > 0 in business logic
    year: Mapped[int] = mapped_column(Integer, nullable=False)   # TODO: Add logic, that year can't be more or less 1900 and 2025
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    transmission: Mapped[TransmissionType] = mapped_column(SAEnum(TransmissionType), nullable=False)
    engine: Mapped[EngineType] = mapped_column(SAEnum(EngineType), nullable=False)
    vin_number: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)  # VIN must be unique
    # TODO Maybe change vin_number from str type to int?

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                 nullable=False)

    # Relationships
    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="car")

    def to_read_model(self) -> CarSchema:
        return CarSchema(
            id=self.id,
            brand=self.brand,
            model=self.model,
            price=self.price,
            year=self.year,
            color=self.color,
            mileage=self.mileage,
            transmission=self.transmission,
            engine=self.engine,
            vin_number=self.vin_number,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
