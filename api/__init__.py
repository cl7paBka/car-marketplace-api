from api.car_routes import cars_api_router
from api.user_routes import users_api_router
from api.order_routes import orders_api_router

#This is an API package
routers = (cars_api_router, users_api_router, orders_api_router)
