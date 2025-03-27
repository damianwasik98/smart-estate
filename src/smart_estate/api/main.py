from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from smart_estate.api.deps import config, get_db
from smart_estate.api.routers import asari
from smart_estate.db.engine import create_tables
from smart_estate.integrations.asari.exceptions import CRMAuthenticationError
from smart_estate.repositories.exceptions import RepositorySaveError


@asynccontextmanager
async def lifespan(app: FastAPI):
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        send_default_pii=True,
    )
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
