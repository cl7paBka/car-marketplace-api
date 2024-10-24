from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.order import OrderCreate, OrderInfo
from src.db import get_db
from src.db.models import OrderStatus
from src.db.repositories.order_repository import OrderRepository
from typing import Optional, Dict

orders_api_router = APIRouter(prefix="/orders")




def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


async def check_for_order_existance(order_id: int, order_repo: OrderRepository):
    pass

# TODO: order endpoints (new order_by_status and others) and universal check for existance function for every type of
#  entities and TESTS + DOCKER + DOCKER.COMPOSE!
