import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from asari_automation_api.repositories.users import UserRepository
from ..conftest import UserFactory


@pytest.mark.asyncio
async def test_returns_user_with_the_same_api_key(
    db: AsyncEngine, user_repository: UserRepository, user_factory: UserFactory
) -> None:
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        user = await user_factory.create_async()

    result = await user_repository.get_by_api_key(user.api_key)
    assert result == user


@pytest.mark.asyncio
async def test_returns_none_when_there_is_no_user_with_given_key(
    db: AsyncEngine, user_repository: UserRepository, user_factory: UserFactory
) -> None:
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        await user_factory.create_async(api_key="1234")

    assert not await user_repository.get_by_api_key("2222")


@pytest.mark.asyncio
async def test_returns_none_when_no_users_in_db(
    user_repository: UserRepository,
) -> None:
    assert not await user_repository.get_by_api_key("1234")
