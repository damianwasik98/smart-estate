from pydantic import Field, SecretStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    API_NAME: str = "Smart Estate API"
    API_VERSION: str = "v1"
    GROQ_API_KEY: SecretStr = Field(...)
    DB_USERNAME: SecretStr = SecretStr("postgres")
    DB_PASSWORD: SecretStr = SecretStr("postgres")
    DB_HOST: str = "localhost"
    DB_NAME: str = "real_estate_automation"
    DB_PORT: int = 5432
    FERNET_KEY: SecretStr = Field(...)
    SENTRY_DSN: HttpUrl | None = None

    model_config = SettingsConfigDict(env_file=".env")
