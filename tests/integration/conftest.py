import pytest
from smart_estate.config import Config


@pytest.fixture
def config() -> Config:
    return Config(FERNET_KEY="P_stpWKjuSOAjBJ4Am5Po5DlQc8W8iYetNzIDrTINgg=")
