from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    API_NAME: str = "Real Estate Agency Automation"
    ASARI_API_KEY: SecretStr = Field(...)
    GROQ_API_KEY: SecretStr = Field(...)
