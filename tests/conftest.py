import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.db.db import Base, get_async_session
from main import app

# Test database configuration
DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost/test_db"
engine_test = create_async_engine(DATABASE_URL, future=True)
TestSession = async_sessionmaker(bind=engine_test, expire_on_commit=False)


# Fixture for setting up and tearing down the test database
@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    """
    Sets up the test database by creating tables before tests
    and dropping them after tests.
    """
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Fixture for overriding the get_async_session dependency
@pytest_asyncio.fixture
async def override_get_async_session():
    """
    Overrides the get_async_session dependency to use the test database session.
    This ensures that each test runs in isolation with a separate session.
    """
    async def _override():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_async_session] = _override


# Fixture for providing an asynchronous HTTP client for testing
@pytest_asyncio.fixture
async def client(override_get_async_session):
    """
    Provides an asynchronous HTTP client for testing FastAPI endpoints.
    Uses ASGITransport to interact directly with the FastAPI application
    without starting an actual server.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
