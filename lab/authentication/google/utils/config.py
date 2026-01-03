from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_TIME: int = 30
    DB_URL: str
    CLIENT_ID_GOOGLE: str
    CLIENT_GOOGLE_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")