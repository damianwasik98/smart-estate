from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from smart_estate.api.auth import get_user_by_api_key
from smart_estate.api.schemas import (
    PhonecallNote,
    PlainCRMCredentials,
)
from smart_estate.db.models import AsariCredentials, User
from smart_estate.integrations.asari.crm_service import AsariCRMService
from smart_estate.repositories.asari_credentials import (
    AsariCredentialsRepository,
)
from smart_estate.api.deps import get_asari_credentials_repo

router = APIRouter(prefix="/asari", tags=["asari"])


@router.post("/authorize")
async def save_asari_credentials(
    credentials: PlainCRMCredentials,
    user: User = Depends(get_user_by_api_key),
    asari_credentials_repository: AsariCredentialsRepository = Depends(
        get_asari_credentials_repo
    ),
):
    asari_creds = AsariCredentials(
        username=credentials.username.get_secret_value(),
        password=credentials.password.get_secret_value(),
        user_id=user.id,
    )
    AsariCRMService(asari_creds)  # login to check if creds are valid
    await asari_credentials_repository.save_credentials(asari_creds)
    return JSONResponse(
        {"message": "Asari credentials saved successfully"},
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/phonecall-note")
async def save_phonecall(
    phonecall_note: PhonecallNote,
    user: User = Depends(get_user_by_api_key),
    asari_credentials_repository: AsariCredentialsRepository = Depends(
        get_asari_credentials_repo
    ),
):
    asari_creds = await asari_credentials_repository.get_by_user_id(user.id)
    crm_service = AsariCRMService(asari_creds)
    await crm_service.save_phonecall_to_crm(phonecall_note)
    return JSONResponse(
        {"message": "Phonecall saved to Asari"},
        status_code=status.HTTP_201_CREATED,
    )
