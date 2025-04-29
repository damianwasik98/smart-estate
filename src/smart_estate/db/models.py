from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


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


class AsariPhonecall(SQLModel, table=True):
    __tablename__ = "asari_phonecalls"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    date: datetime = Field(index=True)
    note: str = Field(...)
    parsed_requirements: dict = Field(
        ..., default_factory=dict, sa_column=Column(JSONB)
    )
