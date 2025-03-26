from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str
    api_key: str = Field(index=True)


class AsariCredentials(SQLModel, table=True):
    __tablename__ = "asari_credentials"
    user_id: int = Field(default=None, primary_key=True, foreign_key="users.id")
    username: str = Field(...)
    password: str = Field(...)
