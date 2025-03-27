from contextlib import asynccontextmanager
from asari_automation_api.api.deps import config, get_db
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from asari_automation_api.api.routers import asari
from asari_automation_api.db.engine import create_tables
from asari_automation_api.integrations.asari.exceptions import CRMAuthenticationError
from asari_automation_api.repositories.exceptions import RepositorySaveError


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    await create_tables(db)
    yield


app = FastAPI(
    title=config.API_NAME,
    root_path=f"/{config.API_VERSION}",
    lifespan=lifespan,
)
app.include_router(asari.router)


@app.exception_handler(RepositorySaveError)
async def repository_save_error_handler(request: Request, exc: RepositorySaveError):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={"message": str(exc)},
    )


@app.exception_handler(CRMAuthenticationError)
async def repository_save_error_handler(request: Request, exc: CRMAuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": str(exc)},
    )
