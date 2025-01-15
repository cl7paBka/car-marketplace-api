from src.api.routes.users import router as users_router
from src.api.routes.cars import router as cars_router
from src.api.routes.orders import router as orders_router


all_routers = [
    users_router,
    cars_router,
    orders_router
]