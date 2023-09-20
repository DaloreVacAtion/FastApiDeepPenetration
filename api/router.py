from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from api.v1.router import v1_router
from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserRead, UserCreate
from core.resources import ServiceResult


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

root_router = APIRouter(prefix="/api/v1")
root_router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Auth'],
)
root_router.include_router(v1_router)


@root_router.get("/ping")
async def ping() -> ServiceResult:
    return ServiceResult(ok=True, message="Pong")
