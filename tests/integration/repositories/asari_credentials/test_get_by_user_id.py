import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from asari_automation_api.repositories.asari_credentials import (
    AsariCredentialsRepository,
)
from ..conftest import AsariCredentialsFactory, UserFactory


@pytest.mark.asyncio
async def test_returns_credentials_when_user_has_asari_credentials(
    asari_credentials_repository: AsariCredentialsRepository,
    db: AsyncEngine,
    user_factory: UserFactory,
    asari_credentials_factory: AsariCredentialsFactory,
) -> None:
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        user = await user_factory.create_async()

        asari_credentials_factory.__async_session__ = session
        credentials = await asari_credentials_factory.create_async(user_id=user.id)

    result = await asari_credentials_repository.get_by_user_id(user.id)
    assert result == credentials


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
