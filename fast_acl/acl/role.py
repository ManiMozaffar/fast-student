from enum import auto

from fast_acl.enums import StrEnum


class UserRoles(StrEnum):
    STUDENT = auto()
    TEACHER = auto()
    ADVISOR = auto()
    ADMIN = auto()
