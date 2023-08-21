from enum import auto

from fast_acl.enums import StrEnum


class RoutesEnum(StrEnum):
    ADD_STUDENT = auto()
    DELETE_STUDENT = auto()
    UPDATE_STUDENT = auto()
    READ_STUDENT = auto()
    EXPEL_STUDENT = auto()
