import pytest

from asari_automation_api.db.engine import AsyncEngine
from asari_automation_api.repositories.users import UserRepository


@pytest.fixture
def user_repository(db: AsyncEngine) -> UserRepository:
    return UserRepository(db)
