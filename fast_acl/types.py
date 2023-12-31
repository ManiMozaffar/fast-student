from typing import NewType
from uuid import UUID

UserId = NewType("UserId", UUID)
StudentId = NewType("StudentId", UUID)
ClassRoomId = NewType("ClassRoomId", UUID)
TeacherId = NewType("TeacherId", UUID)
AdvisorId = NewType("AdvisorId", UUID)
ClassRelationId = NewType("ClassRelationId", UUID)
