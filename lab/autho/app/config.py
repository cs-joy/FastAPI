from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_PRIVATE_KEY_PATH: str = "./private_key.pem"
    JWT_PUBLIC_KEY_PATH: str = "./public_key.pem"
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    # Google OAuth2
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    
    # Apple OAuth2
    APPLE_CLIENT_ID: str
    APPLE_TEAM_ID: str
    APPLE_KEY_ID: str
    APPLE_PRIVATE_KEY_PATH: str = "./apple_private_key.p8"
    APPLE_REDIRECT_URI: str
    
    # Security
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()