from enum import auto

from pydantic_settings import BaseSettings

from fast_acl.enums import StrEnum


class ProductEnvironment(StrEnum):
    PRODUCTION = auto()
    STAGING = auto()
    DEV = auto()


class Algorithms(StrEnum):
    HS256 = auto()


class Settings(BaseSettings):
    # TODO: none of these should be hardcoded, but we did for sake of simplicity

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "HELLO"
    ALGORITHM: str = Algorithms.HS256
    VERSION: int = 1
    ENV: ProductEnvironment = ProductEnvironment.DEV


setting = Settings()
