from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from smart_estate.db.models import *


def create_db(connection_url: str, debug_mode: bool = False) -> AsyncEngine:
    return create_async_engine(connection_url, echo=debug_mode)


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
