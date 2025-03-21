from fastapi import APIRouter, Depends, HTTPException, status

from asari_automation_api.api.auth import get_user_by_token
from asari_automation_api.api.schemas import (
    PhonecallNote,
    PlainCRMCredentials,
)
from asari_automation_api.db.models import User
from asari_automation_api.integrations.asari.authorizer import AsariAuthorizer
from asari_automation_api.integrations.asari.crm_service import AsariCRMService

router = APIRouter(prefix="/asari", tags=["asari"])


@router.post("/authorize")
async def save_asari_credentials(
    credentials: PlainCRMCredentials,
    user: User = Depends(get_user_by_token),
):
    authorizer = AsariAuthorizer(credentials)
    await authorizer.validate_crm_credentials()
    await authorizer.save_crm_credentials_in_db(user.id)


@router.post("/phonecall-note")
async def save_phonecall(
    phonecall_note: PhonecallNote,
    user: User = Depends(get_user_by_token),
):
    try:
        crm_service = AsariCRMService(user.crm_credentials)
    except ValueError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "CRM credentials are invalid for this user",
        )
    await crm_service.save_phonecall_to_crm(phonecall_note)
