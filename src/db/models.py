from datetime import datetime
import enum
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()


# Enums
class Role(enum.Enum):
    customer = 'customer'
    manager = 'manager'
    admin = 'admin'


class EngineType(enum.Enum):
    gasoline = 'gasoline'
    electric = 'electric'
    diesel = 'diesel'


class TransmissionType(enum.Enum):
    manual = 'manual'
    automatic = 'automatic'


class OrderStatus(enum.Enum):
    pending = 'pending'
    completed = 'completed'
    canceled = 'canceled'


# Models
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(SAEnum(Role), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user", foreign_keys="Order.user_id"
    )
    sales_orders: Mapped[list["Order"]] = relationship(
        "Order", foreign_keys="Order.salesperson_id"
    )


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    transmission: Mapped[TransmissionType] = mapped_column(SAEnum(TransmissionType), nullable=False)
    engine: Mapped[EngineType] = mapped_column(SAEnum(EngineType), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    vin_number: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="car")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), nullable=False, default=OrderStatus.pending)

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)
    salesperson_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders", foreign_keys=[user_id])
    car: Mapped["Car"] = relationship("Car", back_populates="orders")
    salesperson: Mapped["User"] = relationship("User", foreign_keys=[salesperson_id], overlaps="sales_orders")

    comments: Mapped[str] = mapped_column(String(255), nullable=True)
