from asari import AsariAPI

from asari_automation_api.api.schemas import PlainCRMCredentials
from asari_automation_api.db.models import User
from asari_automation_api.repositories.users import UserRepository


class AsariAuthorizer:
    def __init__(
        self, credentials: PlainCRMCredentials, user_repository: UserRepository
    ) -> None:
        self._username = credentials.username.get_secret_value()
        self._password = credentials.password.get_secret_value()
        self._user_repository = user_repository

    async def validate_crm_credentials(self) -> None:
        try:
            AsariAPI(email=self._username, password=self._password)
        except Exception:  # TODO: maybe specific error
            raise

    async def save_crm_credentials_in_db(self, user_id: int) -> None:
        await self._user_repository.update_user_crm_credentials(
            user_id,
            credentials={
                "asari": {"username": self._username, "password": self._password}
            },
        )
