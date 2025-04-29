from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from smart_estate.api.auth import get_user_by_api_key
from smart_estate.api.deps import get_asari_credentials_repo, get_asari_phonecall_repo
from smart_estate.api.schemas import (
    PhonecallNote,
    PlainCRMCredentials,
)
from smart_estate.db.models import AsariCredentials, User
from smart_estate.integrations.asari.crm_service import AsariCRMService
from smart_estate.repositories.asari_credentials import (
    AsariCredentialsRepository,
)
from smart_estate.repositories.asari_phonecalls import AsariPhonecallRepository

router = APIRouter(prefix="/asari", tags=["asari"])


@router.get("/check-credentials")
async def check_asari_credentials(
    user: User = Depends(get_user_by_api_key),
    asari_credentials_repository: AsariCredentialsRepository = Depends(
        get_asari_credentials_repo
    ),
):
    credentials = await asari_credentials_repository.get_by_user_id(user.id)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Asari credentials not found"
        )
    return JSONResponse(
        {"message": "Asari credentials exists in db"}, status_code=status.HTTP_200_OK
    )


@router.post("/authorize")
async def save_asari_credentials(
    credentials: PlainCRMCredentials,
    user: User = Depends(get_user_by_api_key),
    asari_credentials_repository: AsariCredentialsRepository = Depends(
        get_asari_credentials_repo
    ),
    asari_phoencall_repository: AsariPhonecallRepository = Depends(
        get_asari_phonecall_repo
    ),
):
    asari_creds = AsariCredentials(
        username=credentials.username.get_secret_value(),
        password=credentials.password.get_secret_value(),
        user_id=user.id,
    )
    AsariCRMService(
        credentials=asari_creds, asari_phonecall_repository=asari_phoencall_repository
    )  # login to check if creds are valid
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
    asari_phoencall_repository: AsariPhonecallRepository = Depends(
        get_asari_phonecall_repo
    ),
):
    asari_creds = await asari_credentials_repository.get_by_user_id(user.id)
    if not asari_creds:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="To use this endpoint you must call auhtorize endpoint first",
        )
    crm_service = AsariCRMService(
        credentials=asari_creds, asari_phonecall_repository=asari_phoencall_repository
    )
    await crm_service.save_phonecall_to_crm(phonecall_note)
    return JSONResponse(
        {"message": "Phonecall saved to Asari"},
        status_code=status.HTTP_201_CREATED,
    )
