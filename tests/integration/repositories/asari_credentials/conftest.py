import pytest

from asari_automation_api.db.engine import AsyncEngine
from asari_automation_api.repositories.asari_credentials import (
    AsariCredentialsRepository,
)


@pytest.fixture
def asari_credentials_repository(db: AsyncEngine) -> AsariCredentialsRepository:
    return AsariCredentialsRepository(db)
