import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from smart_estate.db.models import AsariCredentials
from smart_estate.repositories.asari_credentials import (
    AsariCredentialsRepository,
)
from smart_estate.repositories.exceptions import RepositorySaveError

from ..conftest import AsariCredentialsFactory, UserFactory


@pytest.mark.asyncio
async def test_returns_none_and_saves_credentials_in_db(
    asari_credentials_repository: AsariCredentialsRepository,
    db: AsyncEngine,
    user_factory: UserFactory,
    asari_credentials_factory: AsariCredentialsFactory,
) -> None:
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        user = await user_factory.create_async()

    credentials = asari_credentials_factory.build(user_id=user.id)

    result = await asari_credentials_repository.save_credentials(credentials)
    assert not result

    async with AsyncSession(db) as session:
        query = select(AsariCredentials).where(AsariCredentials.user_id == user.id)
        results = await session.exec(query)
        assert results.first() == credentials


@pytest.mark.asyncio
async def test_raises_save_error_when_no_user_in_db(
    asari_credentials_repository: AsariCredentialsRepository,
    asari_credentials_factory: AsariCredentialsFactory,
) -> None:
    credentials = asari_credentials_factory.build(user_id=999)

    with pytest.raises(RepositorySaveError):
        await asari_credentials_repository.save_credentials(credentials)


@pytest.mark.asyncio
async def test_raises_save_error_when_user_already_has_asari_creds_in_db(
    asari_credentials_repository: AsariCredentialsRepository,
    asari_credentials_factory: AsariCredentialsFactory,
    user_factory: UserFactory,
    db: AsyncEngine,
) -> None:
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        user = await user_factory.create_async()

        asari_credentials_factory.__async_session__ = session
        await asari_credentials_factory.create_async(user_id=user.id)

    new_asari_creds = asari_credentials_factory.build(user_id=user.id)
    with pytest.raises(RepositorySaveError):
        await asari_credentials_repository.save_credentials(new_asari_creds)
