from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    API_NAME: str = "Asari Automation API"
    API_VERSION: str = "v1"
    GROQ_API_KEY: SecretStr = Field(...)
