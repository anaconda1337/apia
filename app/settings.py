from functools import lru_cache

from pydantic import field_validator
from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    NAME: str = Field(..., env="APP_NAME")
    VERSION: str = Field(..., env="APP_VERSION")
    ENV: str = Field(..., env="APP_ENV")

    class Config:
        env_prefix = "APP_"
        case_sensitive = False


class FirebaseSettings(BaseSettings):
    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str

    class Config:
        env_prefix = "FIREBASE_"
        case_sensitive = False

    @field_validator("private_key")
    def replace_newline(cls, v):
        return v.replace("\\n", "\n")


class PostgresSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "postgres"

    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = False


@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache()
def get_firebase_settings() -> FirebaseSettings:
    return FirebaseSettings()


@lru_cache()
def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()
