import time
from typing import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from faker import Faker
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.pytest_plugin import register_fixture

# from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer

from smart_estate.db.engine import AsyncEngine, create_db, create_tables
from smart_estate.db.models import AsariCredentials, AsariPhonecall, User


@pytest.fixture
def postgres_connection_url() -> Iterator[str]:
    with PostgresContainer(
        image="postgres:latest",
        username="postgres",
        password="posstgres",
        dbname="users",
        driver="asyncpg",
    ) as postgres:
        time.sleep(2)
        # TODO: change sleep for something better like wait_for_logs,
        # I tried this approach but wait_for_logs didn't work
        # because db restarted after displaying ready to accept connections
        # I noticed in logs following line:
        # waiting for server to shut down....2025-03-26 17:54:44.172 UTC [55] LOG:  received fast shutdown request

        # wait_for_logs(
        #     postgres, "database system is ready to accept connections", timeout=30
        # )
        yield postgres.get_connection_url()


@pytest_asyncio.fixture
async def db(postgres_connection_url: str) -> AsyncIterator[AsyncEngine]:
    engine: AsyncEngine = create_db(postgres_connection_url, debug_mode=True)
    await create_tables(engine)
    yield engine


@register_fixture
class UserFactory(SQLAlchemyFactory[User]):
    __faker__ = Faker(locale="pl_PL")

    id = None

    @classmethod
    def username(cls):
        return cls.__faker__.user_name()

    @classmethod
    def api_key(cls):
        return cls.__faker__.uuid4()


@register_fixture
class AsariCredentialsFactory(SQLAlchemyFactory[AsariCredentials]):
    __faker__ = Faker(locale="pl_PL")

    @classmethod
    def username(cls):
        return cls.__faker__.user_name()

    @classmethod
    def password(cls):
        return cls.__faker__.password()


@register_fixture
class AsariPhonecallFactory(SQLAlchemyFactory[AsariPhonecall]):
    __faker__ = Faker(locale="pl_PL")
