from typing import Type

from fast_acl.db import Database
from fast_acl.exception import NotAuthorizedError
from fast_acl.repository import ClassroomRepository
from fast_acl.types import ClassRoomId, StudentId, UserId


async def is_allowed(*_, **__):
    return True


async def is_not_allowed(*_, **__):
    raise NotAuthorizedError


async def related_classroom(
    database: Type[Database],
    asked_id: UserId,
    ask_for_id: UserId,
    classroom_id: ClassRoomId,
    **_
):
    repo = ClassroomRepository(database)
    relations = repo.filter_classroom_relations(classroom_id)
    for relation in relations:
        if (is_classroom_teacher := relation.teacher_id == asked_id):
            if not repo.is_student_in_classroom(
                    classroom_id, student_id=StudentId(ask_for_id)
            ):
                raise NotAuthorizedError
            return True

        if (is_self_student := relation.student_id == asked_id and asked_id == ask_for_id):
            return True

    raise NotAuthorizedError
