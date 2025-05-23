import secrets
import warnings
from typing import Annotated, Any, Literal
from typing_extensions import Self

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    HOST: HttpUrl = "http://localhost:8000"

    CORS_ALLOW_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.CORS_ALLOW_ORIGINS] + [
            self.HOST
        ]
    

    PROJECT_NAME: str
    PROJECT_VERSION: str
    SENTRY_DSN: HttpUrl | None = None

    SQLITE_SERVER: str = "sqlite:///./db.sqlite3"
    SQLALCHEMY_DATABASE_URI: str = SQLITE_SERVER
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    @model_validator(mode="after")
    def check_sentry(self) -> Self:
        if self.SENTRY_DSN:
            warnings.warn(
                "Sentry is enabled. Make sure to set the DSN in production."
            )
        return self

    @model_validator(mode="after")
    def check_cors(self) -> Self:
        if not self.CORS_ALLOW_ORIGINS:
            warnings.warn(
                "CORS is disabled. This may cause issues with cross-origin requests."
            )
        return self

    @model_validator(mode="after")
    def check_api_prefix(self) -> Self:
        if not self.API_PREFIX.startswith("/"):
            warnings.warn(
                "API_PREFIX should start with a '/'. "
                "This may cause issues with routing."
            )
        return self

settings = Settings()