import sentry_sdk
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from smart_estate.api.deps import config, get_user_repository
from smart_estate.db.models import User
from smart_estate.repositories.users import UserRepository

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_user_by_api_key(
    key: str = Security(api_key_header),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User | None:
    # what if header does not exist?
    user = await user_repository.get_by_api_key(key)
    if config.SENTRY_DSN:
        sentry_sdk.set_user({"id": user.id, "username": user.username})
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "There is no user associated with this api key",
        )

    return user
