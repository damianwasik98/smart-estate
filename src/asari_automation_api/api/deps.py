from asari_automation_api.repositories.users import UserRepository


async def get_user_repository() -> UserRepository:
    return UserRepository()
