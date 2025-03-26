from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from asari_automation_api.db.models import User
from sqlmodel import select


class UserRepository:
    def __init__(self, db: AsyncEngine) -> None:
        self._db = db

    async def get_by_api_key(self, api_key: str) -> User | None:
        async with AsyncSession(self._db) as session:
            query = select(User).where(User.api_key == api_key)
            results = await session.exec(query)
            return results.first()

    async def update_user_crm_credentials(
        self, user_id: int, credentials: dict
    ) -> None:
        pass
