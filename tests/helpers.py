from httpx import AsyncClient
from sqlalchemy import select, text, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.models import User
from services.users import pwd_context
from tests.factories import UserFactory


async def get_user_token(ac: AsyncClient, username: str, password: str) -> str | None:
    auth = await ac.post('api/v1/users/auth/token', data={
        "username": username,
        "password": password,
    })
    token = auth.json().get('access_token') if auth.status_code == status.HTTP_200_OK else None
    return token


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    users = await session.execute(select(User).where(User.id == user_id))
    user = users.scalars().first()
    return user


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    password: str,
    superuser: bool | None = None,
):
    hashed_password = pwd_context.hash(password)
    user = UserFactory.build(
        username=username,
        email=email,
        age=20,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=superuser if superuser else False,
        is_verified=True,
    )
    # statement = insert(User).values(
    #     username=username,
    #     email=email,
    #     age=15,
    #     hashed_password=hashed_password,
    #     is_active=True,
    #     is_superuser=superuser if superuser else False,
    #     is_verified=True,
    # )
    # await session.execute(statement)
    # await session.commit()
    # query = text(f'select * from public.user where public.user.email = \'{email}\'')
    # user = await session.execute(query)
    # return user.first()
    return user

async def clear_users(
    session: AsyncSession,
):
    statement = text(f'delete from public.user')
    await session.execute(statement)
    await session.commit()
