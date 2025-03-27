from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from asari_automation_api.repositories.asari_credentials import (
    AsariCredentialsRepository,
)
from asari_automation_api.repositories.users import UserRepository
from asari_automation_api.db.engine import create_db
from asari_automation_api.config import Config


config = Config()


def get_db() -> AsyncEngine:
    return create_db(
        f"postgresql+asyncpg://{config.DB_USERNAME.get_secret_value()}:{config.DB_PASSWORD.get_secret_value()}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )


async def get_user_repository(
    db: AsyncEngine = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


async def get_asari_credentials_repo(
    db: AsyncEngine = Depends(get_db),
) -> AsariCredentialsRepository:
    return AsariCredentialsRepository(
        db, fernet_key=config.FERNET_KEY.get_secret_value()
    )
