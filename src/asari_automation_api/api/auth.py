from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from asari_automation_api.api.deps import get_user_repository
from asari_automation_api.db.models import User
from asari_automation_api.repositories.users import UserRepository

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_user_by_api_key(
    key: str = Security(api_key_header),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User | None:
    # what if header does not exist?
    user = await user_repository.get_by_api_key(key)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "There is no user associated with this api key",
        )

    return user
