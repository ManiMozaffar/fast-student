from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY = "HELLO"
    ALGORITHM = "HS256"


setting = Settings()
