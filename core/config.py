from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    APP_NAME: str
    SECRET_KEY: str
    DEBUG: bool
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_URL: str | None = None
    DB_TEST_URL: str | None = None
    AUTH_SECRET_KEY: str

    @field_validator('DB_URL', mode='before')
    def assemble_postgres_url(cls, value: str | None, values: FieldValidationInfo) -> str:
        values = values.data
        if isinstance(value, str):
            return value

        username = values.get('DB_USER')
        password = values.get('DB_PASS')
        host = values.get('DB_HOST')
        port = values.get('DB_PORT')
        db_name = values.get('DB_NAME')
        uri = f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}'
        return uri


settings = Settings()
