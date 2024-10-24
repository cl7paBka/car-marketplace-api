from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserInfo
from src.db import get_db
from src.db.models import Role
from src.db.repositories.user_repository import UserRepository
from typing import Optional, Dict

users_api_router = APIRouter(prefix="/users")


# Dependency to get DB session
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


# TODO: Make universal check for existance func, for every type of entities like user, car or order

async def check_for_user_existence(user_id: int, user_repo: UserRepository):
    existing_user = user_repo.get_user_by_id(user_id)
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


@users_api_router.post("/create", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Create a new user and return the created user's information.

    Returns the created user data and a success message.

    You can choose specific user role like "admin", "manager" or "customer".

    User's email must be unique.
    """
    created_user = user_repo.create_user(user)
    if created_user is not None:
        return {
            "status": "success",
            "message": f"User with ID {created_user.id} created successfully",
            "data": created_user.dict()
        }
    raise HTTPException(status_code=400, detail="User not created")


#
@users_api_router.get("/{user_id}", response_model=Dict)
async def get_user_by_id(user_id: int, user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Retrieve a user by their ID.

    Returns 404 if the user is not found.
    """
    user = user_repo.get_user_by_id(user_id)
    if user is not None:
        return {
            "status": "success",
            "message": f"User with ID {user_id} found.",
            "data": user.dict()
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")


@users_api_router.get("/email/{email}", response_model=Dict)
async def get_user_by_email(email: str, user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Retrieve a user by their email address.

    Returns 404 if the user is not found.
    """
    user = user_repo.get_user_by_email(email)
    if user is not None:
        return {
            "status": "success",
            "message": f"User with email {user.email} found, its ID is {user.id}",
            "data": user.dict()
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")


@users_api_router.get("/", response_model=Dict)
async def get_all_users(user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Retrieve all users from the database.

    Returns a success message with the user data if found, otherwise raises a 404 error.
    """
    all_users = user_repo.get_all_users()
    if all_users is not None:
        data = {user.id: user.dict() for user in all_users}
        return {
            "status": "success",
            "message": "All users retrieved successfully.",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found")


@users_api_router.get("/role/{role}", response_model=Dict)
async def get_users_by_role(user_role: Role, user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Retrieve all users with a specific role (admin, manager, customer).
    """
    all_users_with_specific_role = user_repo.get_users_by_role(user_role)
    if all_users_with_specific_role is not None:
        data = {user.id: user.dict() for user in all_users_with_specific_role}
        return {
            "status": "success",
            "message": f"All users with role {user_role.value} retrieved successfully.",
            "data": data
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users with role {user_role.value} found")


@users_api_router.patch("/update/{user_id}", response_model=Dict)
async def update_user(user_id: int, user_data: UserInfo,
                      user_repo: UserRepository = Depends(get_user_repository)) -> Dict:
    """
    Update user information by their ID. If the user is not found, return 404.
    """
    await check_for_user_existence(user_id, user_repo)

    updated_user = user_repo.update_user_by_id(user_id, user_data)
    if updated_user is not None:
        return {
            "status": "success",
            "message": f"User with ID {user_id} updated successfully.",
            "data": updated_user.dict()
        }


@users_api_router.delete("/delete/{user_id}", response_model=Optional[Dict])
async def delete_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)) -> Optional[Dict]:
    """
    Delete a user by their ID.

    Returns the ID of the deleted user, or 404 if the user is not found.
    """
    await check_for_user_existence(user_id, user_repo)

    deleted_user_id = user_repo.delete_user_by_id(user_id)
    if deleted_user_id is not None:
        return {
            "status": "success",
            "message": f"User with ID {deleted_user_id} deleted successfully."
        }
    raise HTTPException(status_code=400, detail=f"User with ID {user_id} could not be deleted")
