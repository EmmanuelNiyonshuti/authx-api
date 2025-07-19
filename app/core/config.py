from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str
    database_url: str

    api_url: str = "http://testserver/api"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 15

    superuser_username: str
    superuser_email: str
    superuser_password: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
