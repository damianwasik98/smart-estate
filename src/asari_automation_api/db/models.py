from sqlmodel import SQLModel, Field, JSON, Column


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    api_token: str = Field(index=True)
    crm_credentials: dict = Field(sa_column=Column(JSON))
