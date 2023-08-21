# Think of this file as SQL model database

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from fast_acl.acl.role import UserRoles
from fast_acl.types import (
    AdvisorId,
    ClassRelationId,
    ClassRoomId,
    StudentId,
    TeacherId,
    UserId,
)


class User(BaseModel):
    id: UserId = Field(default_factory=uuid.uuid4, frozen=True)
    role: UserRoles
    username: str
    password: str


class Teacher(BaseModel):
    id: TeacherId = Field(default_factory=uuid.uuid4, frozen=True)
    user_id: UserId = Field(default_factory=uuid.uuid4)


class Admin(BaseModel):
    id: TeacherId = Field(default_factory=uuid.uuid4, frozen=True)
    user_id: UserId = Field(default_factory=uuid.uuid4)


class Advisor(BaseModel):
    id: AdvisorId = Field(default_factory=uuid.uuid4, frozen=True)
    user_id: UserId = Field(default_factory=uuid.uuid4)


class Student(BaseModel):
    id: StudentId = Field(default_factory=uuid.uuid4, frozen=True)
    user_id: UserId
    grade: int | None = None
    is_expeled: bool = False


class ClassRoom(BaseModel):
    id: ClassRoomId = Field(default_factory=uuid.uuid4, frozen=True)
    topic: str


class ClassRoomRelation(BaseModel):
    id: ClassRelationId = Field(default_factory=uuid.uuid4, frozen=True)
    classroom_id: ClassRoomId = Field(default_factory=uuid.uuid4)
    student_id: StudentId | None = None
    teacher_id: TeacherId | None = None
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
