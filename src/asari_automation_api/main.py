from fastapi import Depends, FastAPI

from asari_automation_api.asari import AsariService
from asari_automation_api.auth import get_user_by_token
from asari_automation_api.config import Config
from asari_automation_api.models import (
    PhonecallNote,
    User,
)

config = Config()
app = FastAPI(title=config.API_NAME, root_path=f"/{config.API_VERSION}")


@app.post("/phonecall-to-crm")
async def save_phonecall_to_crm(
    phonecall_note: PhonecallNote,
    user: User = Depends(get_user_by_token),
):
    AsariService(user).save_to_asari(phonecall_note)
