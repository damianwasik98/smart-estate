from asari_automation_api.db.models import User
from sqlmodel import select


class UserRepository:
    async def get_by_api_key(self, api_key: str) -> User | None:
        query = select(User).where(User.api_token == token)
        results = session.exec(query)
        return results.first()

    async def update_user_crm_credentials(
        self, user_id: int, credentials: dict
    ) -> None:
        pass
