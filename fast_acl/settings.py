from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "HELLO"
    ALGORITHM: str = "HS256"


setting = Settings()
