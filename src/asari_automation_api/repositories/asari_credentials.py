from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from asari_automation_api.db.models import AsariCredentials
from asari_automation_api.repositories.exceptions import RepositorySaveError


class AsariCredentialsRepository:
    def __init__(self, db: AsyncEngine) -> None:
        self._db = db

    async def get_by_user_id(self, user_id: int) -> AsariCredentials | None:
        query = select(AsariCredentials).where(AsariCredentials.user_id == user_id)
        async with AsyncSession(self._db) as session:
            results = await session.exec(query)
            return results.first()

    async def save_credentials(self, credentials: AsariCredentials) -> None:
        async with AsyncSession(self._db) as session:
            session.add(credentials)
            try:
                await session.commit()
            except IntegrityError:
                raise RepositorySaveError(
                    f"User with id {credentials.user_id} does not exist."
                )
            await session.refresh(credentials)
