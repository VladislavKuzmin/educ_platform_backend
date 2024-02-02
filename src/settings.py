from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, model_validator, SecretStr
from pydantic.alias_generators import to_snake
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import SettingsError

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
GOOGLE_OAUTH_SETTINGS = ROOT_DIR.joinpath("google_oauth_settings.json")
FILES_PATH = ROOT_DIR / "files"


class _Secrets(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore', str_strip_whitespace=True)

    SECRET_API_SESSION: SecretStr


class _ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore', str_strip_whitespace=True,
                                      env_prefix='BACKEND_')

    ENTRYPOINT: str = 'main:make_app'
    HOST: str = '0.0.0.0'
    PORT: int = 8080
    ALGORITHM: str = "HS256"


class _FrontendSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore', str_strip_whitespace=True,
                                      env_prefix='FRONTEND_')

    HOST: str = '127.0.0.1'
    PORT: int = 3000
    AUTH_REDIRECT_URL: str


class _MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore', env_prefix='MONGO_')

    CONNECTION_STRING: str
    USER: str
    PASS: str
    DB_NAME: str


class _GoogleOauthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra='ignore', str_strip_whitespace=True,
                                      alias_generator=to_snake)

    CLIENT_ID: str
    CLIENT_SECRET: str
    AUTH_URI: str
    TOKEN_URI: str
    REDIRECT_URI: str
    SERVER_METADATA_URL: str = 'https://accounts.google.com/.well-known/openid-configuration'
    SCOPE: str = 'openid profile email'
    GRANT_TYPE: str = "authorization_code"
    RESPONSE_TYPE: str = "code"

    @model_validator(mode='before')
    def validate_web(cls, values):
        if "web" in values:
            values["web"]['redirect_uri'] = values["web"]['redirect_uris'][0]
            return values["web"]
        return values

    @classmethod
    def load_from_json(cls) -> '_GoogleOauthSettings':
        try:
            with GOOGLE_OAUTH_SETTINGS.open('r') as file:
                return cls.model_validate_json(file.read(), strict=False)
        except FileNotFoundError:
            raise SettingsError(f"File not found: {cls.config_path}")
        except Exception as e:
            raise SettingsError(f"Error loading settings from file: {e}")


class Settings(BaseModel):
    mongo: _MongoSettings = _MongoSettings()
    server: _ServerSettings = _ServerSettings()
    frontend: _FrontendSettings = _FrontendSettings()
    google_oauth: _GoogleOauthSettings = _GoogleOauthSettings.load_from_json()
    secrets: _Secrets = _Secrets()


@lru_cache
def get_settings() -> Settings:
    return Settings()
