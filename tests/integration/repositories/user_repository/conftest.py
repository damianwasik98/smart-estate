import pytest

from smart_estate.db.engine import AsyncEngine
from smart_estate.repositories.users import UserRepository


@pytest.fixture
def user_repository(db: AsyncEngine) -> UserRepository:
    return UserRepository(db)
