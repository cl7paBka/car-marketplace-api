import asyncio
import uvicorn
import logging
from fastapi import FastAPI

from src.db.db import init_db
from src.api.routers import all_routers

# TODO: Logg only error+
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="Car Marketplace API"
)

for router in all_routers:
    app.include_router(router)


async def main():
    logging.info("Starting init_db()")
    await init_db()

    logging.info("Starting FastAPI app")
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
