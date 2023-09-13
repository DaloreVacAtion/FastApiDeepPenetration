from fastapi import Depends
from fastapi_users import BaseUserManager,  IntegerIDMixin

from auth.models import User
from auth.utils import get_user_db
from core.config import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
