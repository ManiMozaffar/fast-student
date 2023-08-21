from typing import Type

from fast_acl import models
from fast_acl.db import Database
from fast_acl.exception import NotFoundError
from fast_acl.schema import StudentData
from fast_acl.types import ClassRoomId, StudentId


class StudentRepository:
    def get_classroom(
        self, db: Type[Database], class_room_id: ClassRoomId
    ) -> models.ClassRoom:
        classroom: models.ClassRoom = ...  # type : ignore
        if classroom is None:
            raise NotFoundError(obj_id=str(class_room_id))
        return classroom

    def get_student(self, db: Type[Database], student_id: StudentId) -> models.Student:
        ...

    def create_student(
        self, db: Type[Database], student_data: StudentData
    ) -> models.Student:
        ...

    def update_student(
        self, db: Type[Database], student_id: StudentId, student_data: models.Student
    ) -> None:
        student_update_data = student_data.model_dump(exclude_unset=True)
        ...

    def add_student_to_classroom(
        self,
        db: Type[Database],
        student_id: StudentId,
        classroom_id: ClassRoomId,
    ) -> None:
        ...

    def get_relation(
        self, db: Type[Database], student_id, teacher_id
    ) -> models.ClassRoomRelation:
        ...
