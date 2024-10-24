from src.api.car_routes import cars_api_router
from src.api.user_routes import users_api_router
from src.api.order_routes import orders_api_router

#This is an API package
routers = (users_api_router, cars_api_router, orders_api_router)
