from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    API_NAME: str = "Real Estate CRM Automation API"
    API_VERSION: str = "v1"
    GROQ_API_KEY: SecretStr = Field(...)
