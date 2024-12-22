from src.api.users import router as users_router
from src.api.cars import router as cars_router
from src.api.orders import router as orders_router


all_routers = [
    users_router,
    cars_router,
    orders_router
]