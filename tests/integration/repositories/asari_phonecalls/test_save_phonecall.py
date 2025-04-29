import pytest
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from smart_estate.db.models import AsariPhonecall, User
from smart_estate.repositories.asari_phonecalls import AsariPhonecallRepository
from smart_estate.repositories.exceptions import RepositorySaveError

from ..conftest import UserFactory, AsariPhonecallFactory


@pytest.mark.asyncio
async def test_returns_none_and_saves_phonecall_in_db(
    asari_phonecall_repository: AsariPhonecallRepository,
    db: AsyncEngine,
    asari_phonecall_factory: AsariPhonecallFactory,
    user_factory: UserFactory,
) -> None:
    async with AsyncSession(db) as session:
        user_factory.__async_session__ = session
        user = await user_factory.create_async()

    phonecall: AsariPhonecall = asari_phonecall_factory.build(
        user_id=user.id,
        note="łódź śródmieście budżet 500 tysięcy 3 pokoje",
        parsed_requirements={
            "location": "łódź śródmieście",
            "no_of_rooms_min": 3,
            "no_of_rooms_max": 3,
            "price_max": 500000,
        },
    )

    result = await asari_phonecall_repository.save_phonecall(
        user_id=user.id,
        client_name=phonecall.client_name,
        client_phone_number=phonecall.client_phone_number,
        phonecall_note=phonecall.note,
        parsed_requirements=phonecall.parsed_requirements,
    )
    assert not result

    async with AsyncSession(db) as session:
        query = select(AsariPhonecall).where(User.id == user.id)
        results = await session.exec(query)
        phonecall_db = results.first()
        for field in ("user_id", "note", "parsed_requirements"):
            assert getattr(phonecall_db, field) == getattr(phonecall, field)


@pytest.mark.asyncio
async def test_raises_when_user_does_not_exist(
    asari_phonecall_repository: AsariPhonecallRepository,
    asari_phonecall_factory: AsariPhonecallFactory,
) -> None:
    phonecall: AsariPhonecall = asari_phonecall_factory.build()
    with pytest.raises(RepositorySaveError):
        await asari_phonecall_repository.save_phonecall(
            user_id=phonecall.user_id,
            client_name=phonecall.client_name,
            client_phone_number=phonecall.client_phone_number,
            phonecall_note=phonecall.note,
            parsed_requirements=phonecall.parsed_requirements,
        )
