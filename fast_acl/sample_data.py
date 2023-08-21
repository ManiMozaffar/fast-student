# this script should not be inside the application
# but it should be as in one directory back, to mock data

import random
from datetime import datetime, timedelta
from typing import Type

from faker import Faker
from rich import print

from fast_acl.acl.role import UserRoles
from fast_acl.db import Database
from fast_acl.models import (
    Admin,
    Advisor,
    ClassRoom,
    ClassRoomRelation,
    Student,
    Teacher,
    User,
)
from fast_acl.types import ClassRoomId, StudentId, TeacherId

fake = Faker()


def add_sample_data(
    count_admin: int = 1,
    count_classroom: int = 3,
    count_advisor: int = 3,
    count_student: int = 100,
    count_teacher: int = 8,
) -> Type[Database]:
    teachers = [create_teacher() for _ in range(count_teacher)]
    classrooms = [create_classroom() for _ in range(count_classroom)]
    students = [create_student() for _ in range(count_student)]
    advisors = [create_advisor() for _ in range(count_advisor)]
    admins = [create_admin() for _ in range(count_admin)]

    for classroom in classrooms:
        # Assign a random teacher to the classroom
        teacher = random.choice(teachers)
        relation = create_relation(classroom_id=classroom.id, teacher_id=teacher.id)
        Database.add_relation(relation)

        # Assign random students to the classroom
        students_for_classroom = random.sample(
            students, k=random.randint(1, len(students) // 2)
        )
        for student in students_for_classroom:
            relation = create_relation(classroom_id=classroom.id, student_id=student.id)
            Database.add_relation(relation)

    Database.classrooms = classrooms
    Database.teachers = teachers
    Database.students = students
    Database.admins = admins
    Database.advisors = advisors

    print(Database.read_relations())
    return Database


def create_user(role: UserRoles) -> User:
    return User(
        role=role,
        username=fake.name(),
        password=fake.name(),
    )


def create_classroom():
    topics = ["MATH", "PHYSIC", "CHEMISTERY"]
    classroom = ClassRoom(topic=random.choice(topics))
    return classroom


def create_teacher() -> Teacher:
    user = create_user(role=UserRoles.TEACHER)
    return Teacher(user_id=user.id)


def create_student() -> Student:
    user = create_user(role=UserRoles.STUDENT)
    return Student(user_id=user.id)


def create_advisor() -> Advisor:
    user = create_user(role=UserRoles.ADVISOR)
    return Advisor(user_id=user.id)


def create_admin() -> Admin:
    user = create_user(role=UserRoles.ADMIN)
    return Admin(user_id=user.id)


def create_relation(
    classroom_id: ClassRoomId,
    student_id: StudentId | None = None,
    teacher_id: TeacherId | None = None,
) -> ClassRoomRelation:
    if int(student_id is None) + int(teacher_id is None) != 1:
        raise ValueError("XOR of student_id and teacher_id")

    return ClassRoomRelation(
        teacher_id=teacher_id,
        student_id=student_id,
        classroom_id=classroom_id,
        expires_at=datetime.now()
        + timedelta(days=random.randint(0, 30))
        - timedelta(days=random.randint(0, 30)),
    )
