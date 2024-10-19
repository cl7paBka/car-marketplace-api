from fastapi import APIRouter, Depends, HTTPException
from db.repository import UserRepository
from schemas.user import UserCreate, UserInfo, UserInDB
from typing import Dict

users_api_router = APIRouter()


# Add annotation
def get_user_repository():
    """Dependency to get the UserRepository instance."""
    return UserRepository


@users_api_router.get("/users/", response_model=Dict)
async def get_all_users(repo: UserRepository = Depends(get_user_repository())) -> Dict:
    """
    Retrieve all users from the repository.

    Returns a success message with the user data if found, otherwise raises a 404 error.
    """
    all_users = repo.get_all_users()
    if all_users:
        data = {str(user.id): user.dict() for user in all_users}
        return {
            "status": "success",
            "message": "All users retrieved successfully.",
            "data": data
        }
    raise HTTPException(status_code=404, detail="No users found")


@users_api_router.get("/users/get/{user_id}", response_model=Dict)
async def get_user_by_id(user_id: int, repo: UserRepository = Depends(get_user_repository())) -> Dict:
    """
    Retrieve a user by their ID.

    Returns the user data if found, otherwise raises a 404 error.
    """
    user = repo.get_user_by_id(user_id)
    if user:
        return {
            "status": "success",
            "message": f"User with ID {user_id} found.",
            "data": user.dict()
        }
    raise HTTPException(status_code=404, detail="User not found")


@users_api_router.post("/users/create", response_model=Dict)
async def create_user(user: UserCreate, repo: UserRepository = Depends(get_user_repository())) -> Dict:
    """
    Create a new user in the repository.

    Returns the created user data and a success message.
    """
    user_id = repo.create_user(user)
    if user_id:
        return {
            "status": "success",
            "message": "User created successfully.",
            "data": {
                "user_id": user_id,
                **user.dict()
            }
        }
    raise HTTPException(status_code=400, detail="User not created")


@users_api_router.put("/users/update/{user_id}", response_model=Dict)
async def update_user_by_id(user_id: int, user: UserInfo,
                            repo: UserRepository = Depends(get_user_repository())) -> Dict:
    """
    Update an existing user's information by their ID.

    Returns the updated user data if the user is found, otherwise raises a 404 error.
    """
    existing_user = repo.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    repo.update_user_by_id(user_id, user)

    return {
        "status": "success",
        "message": f"User with ID {user_id} updated successfully.",
        "data": UserInDB(id=user_id, **user.dict())
    }


@users_api_router.delete("/users/delete/{user_id}", response_model=Dict)
async def delete_user_by_id(user_id: int, repo: UserRepository = Depends(get_user_repository())) -> Dict:
    """
    Delete a user by their ID from the repository.

    Returns a success message if the user is deleted, otherwise raises a 404 error.
    """
    existing_user = repo.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    deleted_user_id = repo.delete_user_by_id(user_id)
    if deleted_user_id is not None:
        return {
            "status": "success",
            "message": f"User with ID {deleted_user_id} deleted successfully."
        }
    raise HTTPException(status_code=400, detail=f"User with ID {user_id} could not be deleted")
