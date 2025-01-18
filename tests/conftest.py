import os
import asyncio
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from main import app
from src.db.db import Base, get_async_session

# --- Configuration ---
load_dotenv()  # Load environment variables from .env
DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost/test_db")

# Create the engine and the session factory for the test database
engine_test = create_async_engine(DATABASE_URL, future=True)
TestSession = async_sessionmaker(bind=engine_test, expire_on_commit=False)


# --- Event loop fixture ---
@pytest.fixture(scope="session")
def event_loop():
    """
    Creates one shared event loop for the entire test session.

    Why do we need this?
    --------------------
    On Windows, the default event loop policy is ProactorEventLoop, which often
    conflicts with asyncpg when closing or performing network operations. This
    conflict can lead to errors like 'Event loop is closed' or
    "'NoneType' object has no attribute 'send'" because asyncpg might try to send
    or receive data after the loop is already shut down.

    By switching to WindowsSelectorEventLoopPolicy and using a single event loop
    for all tests, we ensure that asyncpg can gracefully handle any remaining
    operations without having the event loop abruptly closed between tests.
    """
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# --- Database-related fixtures ---
@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    """
    Sets up the test database before each test (drops all tables, then creates them).
    After each test, it drops all tables again to ensure a clean state.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield  # Tests will run at this point

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def override_get_async_session():
    """
    Overrides the default get_async_session dependency to use test session
    so that each test runs in isolation with its own transaction scope.
    """
    async def _override():
        async with TestSession() as session:
            try:
                yield session
            except SQLAlchemyError:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_async_session] = _override
    yield
    app.dependency_overrides.pop(get_async_session, None)


# --- HTTP client fixture ---
@pytest_asyncio.fixture
async def client(override_get_async_session):
    """
    Provides an asynchronous HTTP client (AsyncClient) to test FastAPI app.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
