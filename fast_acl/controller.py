from typing import Type

from fast_acl.acl.role import UserRoles
from fast_acl.db import Database
from fast_acl.models import Student
from fast_acl.repository import (
    ClassroomRepository,
    StudentRepository,
    StudentUpdateInfo,
    UserRepository,
)
from fast_acl.types import ClassRoomId, StudentId


class StudentController:
    def __init__(self, database: Type[Database]):
        self.student_repo = StudentRepository(database)
        self.user_repo = UserRepository(database)
        self.classroom_repo = ClassroomRepository(database)

    def get_student(self, student_id: StudentId) -> Student:
        student = self.student_repo.get_student_by_student_id(student_id=student_id)
        return student

    def add_student(
        self, username: str, password: str, classroom_id: ClassRoomId
    ) -> StudentId:
        user = self.user_repo.create_user(
            username, password=password, role=UserRoles.STUDENT
        )
        classroom = self.classroom_repo.get_classroom(classroom_id)
        student = self.student_repo.create_student(
            grade=None, classroom_id=classroom.id, user_id=user.id
        )
        return student.id

    def update_student_grade(self, student_id: StudentId, grade: int) -> None:
        self.student_repo.update_student(
            student_id=student_id, student_data=StudentUpdateInfo(grade=grade)
        )

    def delete_student(self, student_id: StudentId) -> None:
        ...

    def expel_student(self, student_id: StudentId) -> None:
        self.student_repo.expel_student(student_id=student_id)
