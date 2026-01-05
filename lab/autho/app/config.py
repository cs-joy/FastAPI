import os
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List

class Settings(BaseSettings):
    # app configuration
    app_name: str = "autho"
    environment: str = "development"
    db_url: str

    # jwt configuraition
    secret_key: str
    jwt_algorithm: str = "RS256"
    jwt_private_key_path: str
    jwt_public_key_path: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # google configuration
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str | None = None

    # apple configuration
    apple_client_id: str | None = None
    apple_team_id: str | None = None
    apple_key_id: str | None = None
    apple_private_key_path: str | None = None
    apple_redirect_uri: str | None = None

    # security configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"

settings = Settings()


