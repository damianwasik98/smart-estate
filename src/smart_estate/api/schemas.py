from pydantic import BaseModel, SecretStr


class PlainCRMCredentials(BaseModel):
    username: SecretStr
    password: SecretStr


class PhonecallNote(BaseModel):
    client_name: str
    client_phone_number: str
    text: str
