from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'IDP'
    admin_email: str
    items_per_user: int = 50

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()