import pytest
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from smart_estate.config import Config
from smart_estate.db.models import AsariCredentials
from smart_estate.repositories.asari_credentials import (
    AsariCredentialsRepository,
)

from ..conftest import AsariCredentialsFactory, UserFactory


@pytest.mark.asyncio
async def test_returns_decrypted_credentials_when_encrypted_asari_credentials_exist_in_db(
    asari_credentials_repository: AsariCredentialsRepository,
    db: AsyncEngine,
    user_factory: UserFactory,
    asari_credentials_factory: AsariCredentialsFactory,
    config: Config,
) -> None:
    fernet = Fernet(key=config.FERNET_KEY.get_secret_value())
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        username = "test_user"
        password = "test_password"
        user = await user_factory.create_async()
        asari_credentials_factory.__async_session__ = session
        await asari_credentials_factory.create_async(
            username=fernet.encrypt(username.encode()).decode(),
            password=fernet.encrypt(password.encode()).decode(),
            user_id=user.id,
        )
    result = await asari_credentials_repository.get_by_user_id(user.id)
    assert result == AsariCredentials(
        user_id=user.id, username=username, password=password
    )


@pytest.mark.asyncio
async def test_returns_none_when_creds_does_not_exist(
    asari_credentials_repository: AsariCredentialsRepository,
    db: AsyncEngine,
    user_factory: UserFactory,
) -> None:
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        user = await user_factory.create_async()

    result = await asari_credentials_repository.get_by_user_id(user.id)
    assert not result
