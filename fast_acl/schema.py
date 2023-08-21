from datetime import datetime

from pydantic import BaseModel

from fast_acl.acl.role import UserRoles
from fast_acl.types import UserId


class TokenSchema(BaseModel):
    user_id: UserId
    role: UserRoles
    exp: datetime | None = None


class StudentData(BaseModel):
    data: tuple[str, str]


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    user_id: UserId
    role: UserRoles


class ProtectedMessage(BaseModel):
    message: str
