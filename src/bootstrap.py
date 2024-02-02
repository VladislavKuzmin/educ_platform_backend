from contextlib import asynccontextmanager
from typing import AsyncGenerator

from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from integrations.mongodb.client import MongoClient
from settings import get_settings, Settings, FILES_PATH
from transport.routers import *
from utils import AppState


@asynccontextmanager
async def _lifespan(
        app: FastAPI,
) -> AsyncGenerator[None, None]:
    settings = get_settings()
    FILES_PATH.mkdir(exist_ok=True)
    oauth_settings = settings.google_oauth.model_dump(exclude={"CLIENT_ID", "CLIENT_SECRET"}, by_alias=True)
    oauth = OAuth(config=None)
    oauth.register(
        name='google',
        client_id=settings.google_oauth.CLIENT_ID,
        client_secret=settings.google_oauth.CLIENT_SECRET,
        server_metadata_url=settings.google_oauth.SERVER_METADATA_URL,
        client_kwargs=oauth_settings,
    )
    AppState(oauth=oauth)
    mongo_client = MongoClient()
    yield
    mongo_client.close_client()


def _setup_api_routers(
        app: FastAPI,
) -> None:
    app.include_router(client_router)
    app.include_router(oauth_router)
    app.include_router(file_router)


def _setup_middlewares(
        app: FastAPI,
        settings: Settings
):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secrets.SECRET_API_SESSION,
    )


def make_app() -> FastAPI:
    app = FastAPI(
        lifespan=_lifespan,
    )
    settings = get_settings()

    _setup_middlewares(app, settings)
    _setup_api_routers(app)

    return app
