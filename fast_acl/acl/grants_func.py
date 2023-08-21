from typing import Type

from fast_acl.db import Database
from fast_acl.exception import NotAuthorizedError
from fast_acl.repository import StudentRepository
from fast_acl.types import ClassRoomId


async def is_allowed(**_):
    return True


async def is_not_allowed(asked_id, **_):
    raise NotAuthorizedError(asked_id)


async def related_classroom(
    database: Type[Database], asked_id, ask_for_id: ClassRoomId, **_
):
    for relation in database.relations:
        if relation.classroom_id == ask_for_id:
            repo = StudentRepository()
            classroom = repo.get_classroom(database, ask_for_id)
            relation = repo.get_relation(database, classroom.id, asked_id)
            if relation.teacher_id == asked_id:
                return True

            if relation.student_id == asked_id and asked_id == ask_for_id:
                return True

    raise NotAuthorizedError(asked_id)
