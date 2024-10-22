from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import declarative_base, relationship
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

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(SAEnum(Role), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    # orders = relationship("Order", back_populates="user")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(50), nullable=False)
    mileage = Column(Integer, nullable=False)
    transmission = Column(SAEnum(TransmissionType), nullable=False)
    engine = Column(SAEnum(EngineType), nullable=False)
    price = Column(Integer, nullable=False)
    vin_number = Column(String(17), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    # orders = relationship("Order", back_populates="car")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    status = Column(SAEnum(OrderStatus), nullable=False, default=OrderStatus.pending)

    # Foreign Keys
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    # salesperson_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    # user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    # car = relationship("Car", back_populates="orders")
    # salesperson = relationship("User", foreign_keys=[salesperson_id])

    comments = Column(String(255), nullable=True)
