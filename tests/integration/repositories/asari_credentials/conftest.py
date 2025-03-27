import pytest

from smart_estate.config import Config
from smart_estate.db.engine import AsyncEngine
from smart_estate.repositories.asari_credentials import (
    AsariCredentialsRepository,
)


@pytest.fixture
def asari_credentials_repository(
    db: AsyncEngine, config: Config
) -> AsariCredentialsRepository:
    return AsariCredentialsRepository(
        db, fernet_key=config.FERNET_KEY.get_secret_value()
    )
