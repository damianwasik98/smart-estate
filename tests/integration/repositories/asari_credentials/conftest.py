import pytest

from asari_automation_api.config import Config
from asari_automation_api.db.engine import AsyncEngine
from asari_automation_api.repositories.asari_credentials import (
    AsariCredentialsRepository,
)


@pytest.fixture
def asari_credentials_repository(
    db: AsyncEngine, config: Config
) -> AsariCredentialsRepository:
    return AsariCredentialsRepository(
        db, fernet_key=config.FERNET_KEY.get_secret_value()
    )
