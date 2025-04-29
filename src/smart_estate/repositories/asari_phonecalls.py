from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from smart_estate.db.models import AsariPhonecall
from smart_estate.repositories.exceptions import RepositorySaveError


class AsariPhonecallRepository:
    def __init__(self, db: AsyncEngine) -> None:
        self._db = db

    async def save_phonecall(
        self,
        user_id: int,
        client_name: str,
        client_phone_number: str,
        phonecall_note: str,
        parsed_requirements: dict,
    ) -> None:
        async with AsyncSession(self._db) as session:
            phonecall = AsariPhonecall(
                date=datetime.now(),
                user_id=user_id,
                client_name=client_name,
                client_phone_number=client_phone_number,
                note=phonecall_note,
                parsed_requirements=parsed_requirements,
            )
            session.add(phonecall)
            try:
                await session.commit()
            except IntegrityError:
                raise RepositorySaveError(
                    f"Can't save phonecall for user with id {user_id}"
                )
            await session.refresh(phonecall)
