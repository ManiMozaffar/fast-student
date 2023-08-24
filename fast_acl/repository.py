import random
from datetime import datetime, timedelta
from typing import Type, TypedDict

from fast_acl import models
from fast_acl.acl.role import UserRoles
from fast_acl.db import Database
from fast_acl.exception import NotFoundError
from fast_acl.types import ClassRoomId, StudentId, UserId


class StudentUpdateInfo(TypedDict, total=False):
    is_expeled: bool
    grade: int


class ClassroomRepository:
    def __init__(self, db: Type[Database]) -> None:
        self.db = db

    def get_random_classroom(self) -> models.ClassRoom:
        all_classes = self.db.read_classrooms()
        if not all_classes:
            raise NotFoundError(obj_id="'random classroom'")
        return random.choice(all_classes)

    def get_classroom(
        self,
        classroom_id: ClassRoomId,
    ) -> models.ClassRoom:
        classroom = next(
            (
                classroom
                for classroom in self.db.read_classrooms()
                if classroom.id == classroom_id
            ),
            None,
        )
        if not classroom:
            raise NotFoundError(obj_id=classroom_id)
        return classroom

    def filter_classroom_relations(
        self, classroom_id: ClassRoomId
    ) -> list[models.ClassRoomRelation]:
        relations = [
            relation
            for relation in self.db.read_relations()
            if relation.classroom_id == classroom_id
        ]
        return relations

    def is_student_in_classroom(
        self, classroom_id: ClassRoomId, student_id: StudentId
    ) -> bool:
        relation_generator = (
            relation
            for relation in self.db.read_relations()
            if relation.classroom_id == classroom_id
            and relation.student_id == student_id  # noqa
        )
        result = next(relation_generator, None)
        return True if result else False


class UserRepository:
    def __init__(self, db: Type[Database]) -> None:
        self.db = db

    def create_user(self, username: str, password: str, role: UserRoles) -> models.User:
        user = models.User(username=username, password=password, role=role)
        self.db.add_user(user)
        return user

    def get_user(self, user_id: UserId) -> models.User:
        user = next(
            (user for user in self.db.read_users() if user.id == user_id),
            None,
        )
        if not user:
            raise NotFoundError(obj_id=user_id)
        return user


class StudentRepository:
    def __init__(self, db: Type[Database]) -> None:
        self.db = db

    def get_student_by_student_id(
        self,
        student_id: StudentId,
    ) -> models.Student:
        student = next(
            (
                student
                for student in self.db.read_students()
                if student.id == student_id
            ),
            None,
        )
        if not student:
            raise NotFoundError(obj_id=student_id)
        return student

    def get_all_students_from_classroom(
        self,
        classroom_id: ClassRoomId,
    ) -> list[models.Student]:
        student_ids = [
            relation.student_id
            for relation in self.db.read_relations()
            if relation.classroom_id == classroom_id and relation.student_id
        ]
        students = [
            student for student in self.db.read_students() if student.id in student_ids
        ]
        return students

    def create_student(
        self,
        grade: int | None,
        classroom_id: ClassRoomId,
        user_id: UserId,
    ) -> models.Student:
        student = models.Student(user_id=user_id, grade=grade)
        self.db.add_student(student)
        self.db.add_relation(
            models.ClassRoomRelation(
                classroom_id=classroom_id,
                student_id=student.id,
                expires_at=datetime.now() + timedelta(days=365),
            )
        )
        return student

    def update_student(
        self, student_id: StudentId, student_data: StudentUpdateInfo
    ) -> None:
        student = self.get_student_by_student_id(student_id)
        for key, value in student_data.items():
            setattr(student, key, value)
        return None

    def add_student_to_classroom(
        self,
        student_id: StudentId,
        classroom_id: ClassRoomId,
    ) -> None:
        relation = models.ClassRoomRelation(
            student_id=student_id,
            classroom_id=classroom_id,
            expires_at=datetime.now() + timedelta(days=365),
        )
        self.db.add_relation(relation)
        return None

    def expel_student(self, student_id: StudentId) -> None:
        student_data = StudentUpdateInfo(is_expeled=True)
        self.update_student(student_id, student_data)
        return None
