from fastapi import APIRouter, Depends
from typing import Annotated
from src.schemas.users import (
    UserCreate,
    UserUpdate)
from src.services.users import UsersService
from src.api.dependencies import users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/create")
async def create_user(
        user: UserCreate,
        service: Annotated[UsersService, Depends(users_service)]
):
    created_user_id = await service.create_user(user)
    return {
        "status": "success",
        "message": f"Created user with ID: {created_user_id}"
    }


@router.get("/")
async def get_all_users(service: Annotated[UsersService, Depends(users_service)]):
    all_users = await service.get_all_users()
    return {
        "status": "success",
        "message": f"All users retrieved",
        "data": all_users
    }
