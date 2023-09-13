from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from core.config import settings

bearer_transport = BearerTransport(tokenUrl='api/v1/users/auth/token')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.AUTH_SECRET_KEY, lifetime_seconds=60 * 20)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
