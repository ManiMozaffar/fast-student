from pydantic import BaseModel, Field

from fast_acl.acl.role import UserRoles
from fast_acl.types import StudentId, UserId


class TokenSchema(BaseModel):
    user_id: UserId
    role: UserRoles
    exp: int | None = None


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    user_id: UserId
    role: UserRoles


class ProtectedMessage(BaseModel):
    message: str


class StudetnInput(BaseModel):
    username: str
    password: str


class StudetnCreationOutput(BaseModel):
    student_id: StudentId


class StudentUpdateInput(BaseModel):
    grade: int = Field(gt=0, lt=101)
