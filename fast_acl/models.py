# Think of this file as SQL model database

from datetime import datetime

from pydantic import BaseModel, Field

from fast_acl.acl.role import UserRoles
from fast_acl.types import ClassRoomId, StudentId, TeacherId, UserId


class User(BaseModel):
    id: UserId
    role: UserRoles
    username: str
    password: str


class Teacher(BaseModel):
    user_id: UserId
    classroom_id: ClassRoomId


class Advisor(BaseModel):
    user_id: UserId


class Student(BaseModel):
    id: StudentId
    user_id: UserId
    classroom_id: ClassRoomId
    grade: int


class ClassRoom(BaseModel):
    id: ClassRoomId
    teacher_id: TeacherId


class ClassRoomRelation(BaseModel):
    classroom_id: ClassRoomId
    student_id: StudentId
    teacher_id: TeacherId
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
