from fastapi import APIRouter

users_api_router = APIRouter()


@users_api_router.get("/users/get/{user_id}")
async def get_user_by_id():
    pass


@users_api_router.post("/users/create")
async def create_user():
    pass


@users_api_router.put("/users/update/{user_id}")
async def update_user():
    pass


@users_api_router.delete("/users/delete/{user_id}")
async def delete_user():
    pass


@users_api_router.get("/users")
async def get_all_users():
    pass