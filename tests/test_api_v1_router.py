from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.users import get_user_by_id
from tests.services import create_user, get_user_cookies, clear_users


async def test_delete_user_when_user_is_admin(
    async_client: AsyncClient,
    session: AsyncSession,
):
    user_id = await create_user(session, 'test_user', 'test_user@gmail.com', 'test123')
    await create_user(session, 'test_user_admin', 'test_admin@gmail.com', 'test123', superuser=True)
    cookie = await get_user_cookies(async_client, 'test_admin@gmail.com', 'test123')
    response = await async_client.delete(
        f'api/v1/users/{user_id}',
        headers={
            'accept': 'application/json',
        },
        cookies={
            'IDP': str(cookie)
        }
    )
    not_existing_user = await get_user_by_id(user_id, session)
    assert response is not None
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not_existing_user is None
    await clear_users(session)


async def test_get_user_by_username_when_user_is_unauthorized(
        async_client: AsyncClient,
        session: AsyncSession,
):
    response = await async_client.get('api/v1/users?username=test')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_user_by_username_when_user_is_authorized(
    async_client: AsyncClient,
    session: AsyncSession,
):
    await create_user(session, 'test_user', 'test_email@gmail.com', 'test123')
    cookie = await get_user_cookies(async_client, 'test_email@gmail.com', 'test123')
    res = await async_client.get(
        'api/v1/users?username=test_user',
        headers={
            'accept': 'application/json',
        },
        cookies={
            'IDP': str(cookie)
        }
    )
    response = res.json()
    assert response is not None
    assert response['age'] == 15
    assert response.get('password') is None
    await clear_users(session)
