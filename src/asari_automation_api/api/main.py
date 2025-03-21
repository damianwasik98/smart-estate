from fastapi import FastAPI
from asari_automation_api.api.config import Config
from asari_automation_api.api.routers import asari

config = Config()
app = FastAPI(title=config.API_NAME, root_path=f"/{config.API_VERSION}")
app.include_router(asari.router)
