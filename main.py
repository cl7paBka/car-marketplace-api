import asyncio
import uvicorn
from fastapi import FastAPI
from api.car_routes import cars_api_router
from db.initialize import init_db
from db.repository import CarRepository
from api import routers

app = FastAPI()

for router in routers:
    app.include_router(router)


async def main():
    init_db()

    repo = CarRepository()

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
