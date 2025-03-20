from fastapi import Security
from fastapi.security import APIKeyHeader
from sqlmodel import select

from asari_automation_api.models import User

api_key_header = APIKeyHeader("X-API-Key")


def get_user_by_token(token: str = Security(api_key_header)) -> User | None:
    query = select(User).where(User.api_token == token)
    results = session.exec(query)
    user = results.first()
    if not user:
        raise HTTPException(403, "Not authorized")
    return user
