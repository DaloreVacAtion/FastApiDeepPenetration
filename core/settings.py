"""
*********************
Модуль app->core->settings.py \n
Базовые настройки приложения
*********************
"""
import secrets
from starlette.config import Config

config = Config(".env")


# ####### Main application settings #########
ENV = config.get("ENV", cast=str, default="production")
DEBUG: bool = config.get("DEBUG", cast=bool, default=True)

# ################## Auth ###################
SECRET_AUTH_TOKEN = config.get("SECRET_AUTH_TOKEN", cast=str, default=secrets.token_urlsafe(32))
