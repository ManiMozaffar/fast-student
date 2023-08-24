import pytest

from fast_acl.acl.grants_func import (
    NotAuthorizedError,
    is_allowed,
    is_not_allowed,
    related_classroom,
)
from fast_acl.db import Database
from fast_acl.sample_data import (
    create_classroom,
    create_relation,
    create_student,
    create_teacher,
)
from fast_acl.types import UserId


@pytest.fixture(autouse=True)
def prepare_test():
    classrooms = [create_classroom() for _ in range(2)]
    students = [create_student() for _ in range(4)]
    teachers = [create_teacher() for _ in range(2)]
    Database.classrooms = classrooms
    Database.students = students
    Database.teachers = teachers

    for student in students[0:2]:
        Database.add_relation(
            create_relation(classroom_id=classrooms[0].id, student_id=student.id)
        )
        Database.add_relation(
            create_relation(classroom_id=classrooms[0].id, teacher_id=teachers[0].id)
        )

    for student in students[2:4]:
        Database.add_relation(
            create_relation(classroom_id=classrooms[1].id, student_id=student.id)
        )
        Database.add_relation(
            create_relation(classroom_id=classrooms[1].id, teacher_id=teachers[1].id)
        )

    return Database


@pytest.mark.asyncio
class TestACL:
    async def test_is_allowed(self):
        assert await is_allowed() is True

    async def test_is_not_allowed(self):
        with pytest.raises(NotAuthorizedError):
            await is_not_allowed()

    async def test_related_classroom_with_student(self):
        assert (
            await related_classroom(
                database=Database,
                asked_id=UserId(Database.students[3].id),
                ask_for_id=UserId(Database.students[3].id),
                classroom_id=Database.classrooms[1].id,
            )
            is True
        ), "Student doesn't have access to itself"

        with pytest.raises(NotAuthorizedError):
            # Student doesn't have access to itself but in another classroom that he isn't there
            await related_classroom(
                database=Database,
                asked_id=UserId(Database.students[3].id),
                ask_for_id=UserId(Database.students[3].id),
                classroom_id=Database.classrooms[0].id,
            )

        with pytest.raises(NotAuthorizedError):
            # Student doesn't have access to other students in same classroom
            await related_classroom(
                database=Database,
                asked_id=UserId(Database.students[3].id),
                ask_for_id=UserId(Database.students[2].id),
                classroom_id=Database.classrooms[0].id,
            )

        with pytest.raises(NotAuthorizedError):
            # Student doesn't have access to other students in another classroom
            await related_classroom(
                database=Database,
                asked_id=UserId(Database.students[3].id),
                ask_for_id=UserId(Database.students[1].id),
                classroom_id=Database.classrooms[1].id,
            )

    async def test_related_classroom_with_teacher(self):
        assert (
            await related_classroom(
                database=Database,
                asked_id=UserId(Database.teachers[0].id),
                ask_for_id=UserId(Database.students[0].id),
                classroom_id=Database.classrooms[0].id,
            )
            is True
        ), "Teacher doesn't have access to classroom of himself"

        with pytest.raises(NotAuthorizedError):
            # Teacher doesn't have access to student of his classroom in another classroom that
            # the teacher isn't there.
            await related_classroom(
                database=Database,
                asked_id=UserId(Database.teachers[0].id),
                ask_for_id=UserId(Database.students[0].id),
                classroom_id=Database.classrooms[1].id,
            )

        with pytest.raises(NotAuthorizedError):
            # Teacher doesn't have access to student that aren't connected to his classroom
            await related_classroom(
                database=Database,
                asked_id=UserId(Database.teachers[0].id),
                ask_for_id=UserId(Database.students[3].id),
                classroom_id=Database.classrooms[0].id,
            )
