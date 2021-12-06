import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, RedisDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "localhost"
    SERVER_HOST: AnyHttpUrl = "http://localhost:8080"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost", "http://localhost:8080", "http://localhost:8081", "http://localhost:4200", "http://localhost:3000"]
    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ENV: str = "prod"
    PROJECT_NAME: str = "cryptobot-binance"
    SENTRY_DSN: Optional[HttpUrl] = ""
    LOG_LEVEL: str = "INFO"

    API_URL: AnyHttpUrl = "http://localhost:8080/api/v1"
    API_KEY_NAME: str = "access_token"
    API_KEY: Optional[str]
    
    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    REDIS_SENTINEL_SERVER: str = os.getenv("REDIS_USER", "localhost")
    REDIS_SENTINEL_PORT: str = os.getenv("REDIS_SENTINEL_PORT", "5432")
    REDIS_USER: str = os.getenv("REDIS_USER", "cryptobot")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "cryptobot")
    REDIS_DATABASE: str = os.getenv("REDIS_PASSWORD", "cryptobot")
    REDIS_URI: Optional[RedisDsn] = None

    @validator("REDIS_URI", pre=True)
    def assemble_cache_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            user=values.get("REDIS_USER"),
            password=values.get("REDIS_PASSWORD"),
            host=values.get("REDIS_SENTINEL_SERVER"),
            port=values.get("REDIS_SENTINEL_PORT"),
            path=f"/{values.get('REDIS_DATABASE') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    USER_TEST_EMAIL: EmailStr = "test@cryptobot.fr"
    USER_TEST_FIRSTNAME: str = "Test"
    USER_TEST_PASSWORD: str = "test"

    USER_ADMIN_EMAIL: EmailStr = "admin@cryptobot.fr"
    USER_ADMIN_FIRSTNAME: str = "Admin"
    USER_ADMIN_PASSWORD: str = "admin"

    USERS_OPEN_REGISTRATION: bool = True

    class Config:
        case_sensitive = True


settings = Settings()