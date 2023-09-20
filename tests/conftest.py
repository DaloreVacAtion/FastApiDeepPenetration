import asyncio
from typing import AsyncGenerator, AsyncIterator

import pytest
from fastapi.testclient import TestClient
from fastapi_users import FastAPIUsers
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from core.config import settings
from db.database import Base, get_async_session
from main import app
from tests.factories import UserModelFactory

metadata = Base.metadata


engine_test = create_async_engine(settings.DB_TEST_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata.bind = engine_test

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> None:
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
async def get_db() -> AsyncIterator[AsyncConnection]:
    async with engine_test.begin() as conn:
        yield conn


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(name="session")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True)
async def _setup_factories(session) -> None:
    UserModelFactory.save_db_session(session=session)
