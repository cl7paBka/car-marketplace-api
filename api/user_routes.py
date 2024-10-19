from fastapi import APIRouter, Depends, HTTPException
from db.repository import UserRepository
from schemas.user import UserCreate, UserInfo, UserInDB

users_api_router = APIRouter()


def get_user_repository():
    return UserRepository


@users_api_router.get("/users/")
async def get_all_users(repo: UserRepository = Depends(get_user_repository())):
    all_users = repo.get_all_users()
    if all_users:
        data = {user.id: user.dict() for user in all_users}
        return {
            "status": "success",
            "message": "All users extracted successfully",
            "data": data
        }
    raise HTTPException(status_code=404, detail=f"No users found")


@users_api_router.get("/users/get/{user_id}")
async def get_user_by_id(user_id: int, repo: UserRepository = Depends(get_user_repository())):
    user = repo.get_user_by_id(user_id)
    if user:
        return {
            "status": "Success",
            "message": f"User with id {user_id} found",
            "data": user
        }
    raise HTTPException(status_code=404, detail="User not found")


@users_api_router.post("/users/create")
async def create_user(user: UserCreate, repo: UserRepository = Depends(get_user_repository())):
    user_id = repo.create_user(user)
    if user_id:
        return {
            "status": "Success",
            "message": "User created successfully",
            "data": {
                "user_id": user_id,
                **user.dict()
            }
        }
    raise HTTPException(status_code=404, detail=f"User not created")


@users_api_router.put("/users/update/{user_id}")
async def update_user_by_id(user_id: int, user: UserInfo, repo: UserRepository = Depends(get_user_repository())):
    existing_user = repo.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    repo.update_user_by_id(user_id, user)
    return {
        "status": "Success",
        "message": f"User with id {user_id} has been updated successfully",
        "data": UserInDB(id=user_id, **user.dict())
    }


@users_api_router.delete("/users/delete/{user_id}")
async def delete_user_by_id(user_id: int, repo: UserRepository = Depends(get_user_repository())):
    existing_user = repo.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    deleted_user_id = repo.delete_user_by_id(user_id)
    if deleted_user_id is not None:
        return {
            "status": "success",
            "message": f"User with id {deleted_user_id} has been deleted successfully"
        }
    raise HTTPException(status_code=404, detail=f"User with id {user_id} has not been deleted")
