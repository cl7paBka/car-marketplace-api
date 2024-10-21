import asyncio
import uvicorn
from fastapi import FastAPI
from src.db.initialize import init_db
from src.db.repository import CarRepository
from src.api import routers

# Create a FastAPI instance
app = FastAPI()

# Include all routers from the API package
for router in routers:
    app.include_router(router)


async def main():
    """
    Initialize the database and start the FastAPI application.

    This function sets up the database and starts the server using Uvicorn.
    It is called when the script is run as the main module.
    """
    init_db()

    repo = CarRepository()

    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)


if __name__ == "__main__":
    # Run the main function asynchronously
    asyncio.run(main())
