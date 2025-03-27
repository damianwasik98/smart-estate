from cryptography.fernet import Fernet
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from smart_estate.db.models import AsariCredentials
from smart_estate.repositories.exceptions import RepositorySaveError


class AsariCredentialsRepository:
    def __init__(self, db: AsyncEngine, fernet_key: str) -> None:
        self._db = db
        self._cipher = Fernet(key=fernet_key)

    async def get_by_user_id(self, user_id: int) -> AsariCredentials | None:
        query = select(AsariCredentials).where(AsariCredentials.user_id == user_id)
        async with AsyncSession(self._db) as session:
            results = await session.exec(query)
            creds = results.first()
            if creds:
                creds.username = self._cipher.decrypt(creds.username).decode()
                creds.password = self._cipher.decrypt(creds.password).decode()
            return creds

    async def save_credentials(self, credentials: AsariCredentials) -> None:
        credentials.username = self._cipher.encrypt(
            credentials.username.encode()
        ).decode()
        credentials.password = self._cipher.encrypt(
            credentials.password.encode()
        ).decode()
        async with AsyncSession(self._db) as session:
            session.add(credentials)
            try:
                await session.commit()
            except IntegrityError:
                raise RepositorySaveError(
                    f"Can't save credentials for user {credentials.user_id}"
                )
            await session.refresh(credentials)
