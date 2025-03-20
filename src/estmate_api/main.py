from fastapi import Depends, FastAPI

from estmate_api.asari import AsariService
from estmate_api.auth import get_user_by_token
from estmate_api.config import Config
from estmate_api.models import (
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
