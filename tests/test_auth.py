from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.users import create_user, clear_users


async def test_register_user_when_user_exist(async_client: AsyncClient):
    create_data = {
        'email': 'testmail@gmail.com',
        'password': 'string',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'username': 'string',
    }
    await async_client.post('api/v1/auth/register', json=create_data)
    second_user = await async_client.post('api/v1/auth/register', json=create_data)
    assert second_user.json()['detail'] == 'REGISTER_USER_ALREADY_EXISTS'


async def test_register_user_when_data_is_correct(async_client: AsyncClient):
    response = await async_client.post('api/v1/auth/register', json={
        'email': 'test@mail.ru',
        'password': 'string123',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
        'username': 'string'
    })

    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data.get('password') is None


async def test_login_with_bad_username(
        async_client: AsyncClient,
        session: AsyncSession,
):
    await create_user(session, 'test_user', 'test_user@gmail.com', 'test123')
    response = await async_client.post('api/v1/users/auth/token', data={
        'username': 'incorrect_user',
        'password': 'test123',
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Не смогли валидировать входящие данные.'
    await clear_users(session)


async def test_login_with_bad_password(
        async_client: AsyncClient,
        session: AsyncSession,
):
    user = await create_user(session, 'test_user', 'test_user@gmail.com', 'test123')
    response = await async_client.post('api/v1/users/auth/token', data={
        'username': user.username,
        'password': 'incorrect_password',
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Не смогли валидировать входящие данные.'
    await clear_users(session)


async def test_login_success(
    async_client: AsyncClient,
    session: AsyncSession,
):
    user = await create_user(session, 'test_user', 'test_user@gmail.com', 'test123')
    res = await async_client.post('api/v1/users/auth/token', data={
        'username': user.username,
        'password': 'test123',
    })
    assert res.status_code == 200
    response = res.json()
    assert {'access_token', 'token_type'}.issubset(set(response.keys()))
    assert response['token_type'] == 'bearer'
