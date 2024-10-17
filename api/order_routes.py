from fastapi import APIRouter

users_api_router = APIRouter()


@users_api_router.get("/orders/get/{user_id}")
async def get_order_by_id():
    pass

