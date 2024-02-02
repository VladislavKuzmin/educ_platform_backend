from authlib.integrations.starlette_client import OAuth
from singleton_decorator import singleton

from settings import Settings, get_settings


@singleton
class AppState:
    oauth: OAuth
    settings: Settings

    def __init__(self, oauth: OAuth) -> None:
        self.oauth: OAuth = oauth
        self.settings: Settings = get_settings()


async def get_app_state() -> AppState:
    return AppState()
