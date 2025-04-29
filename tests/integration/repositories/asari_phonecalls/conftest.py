import pytest

from smart_estate.db.engine import AsyncEngine
from smart_estate.repositories.asari_phonecalls import AsariPhonecallRepository


@pytest.fixture
def asari_phonecall_repository(db: AsyncEngine) -> AsariPhonecallRepository:
    return AsariPhonecallRepository(db)
