from typing import Type

from fast_acl import models
from fast_acl.db import Database
from fast_acl.exception import NotFoundError
from fast_acl.repository import StudentRepository
from fast_acl.types import ClassRoomId, StudentId


class StudentController:
    repo = StudentRepository()

    def get_student(
        self,
        db: Type[Database],
        classroom_id: None | ClassRoomId = None,
        student_id: StudentId | None = None,
    ) -> models.Student:
        if classroom_id:
            ...
        elif student_id:
            ...
        else:
            raise NotFoundError(...)

    def get_all_students_from_school(self, db: Type[Database]) -> list[models.Student]:
        ...

    def add_student_to_classroom(
        self, db: Type[Database], student: models.Student, classroom_id: ClassRoomId
    ) -> None:
        try:
            student = self.get_student()
        except NotFoundError:
            student = None

        if student is None:
            student = self.repo.create_student()

        self.repo.add_student_to_classroom(student)
        return None

    def update_student_grade(
        self, db: Type[Database], student_id: StudentId, grade: int
    ) -> None:
        ...

    def delete_student(self, db: Type[Database], student_id: StudentId) -> None:
        ...
