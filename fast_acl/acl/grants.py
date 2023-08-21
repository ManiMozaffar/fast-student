from enum import auto

from fast_acl.acl import grants_func as acl
from fast_acl.enums import StrEnum


class PermissionGrants(StrEnum):
    IS_ALLOWED = auto()
    NOT_ALLOWED = auto()

    RELATED_CLASSROOM = auto()


GRANT_MAPPER = {
    PermissionGrants.IS_ALLOWED: acl.is_allowed,
    PermissionGrants.NOT_ALLOWED: acl.is_not_allowed,
    PermissionGrants.RELATED_CLASSROOM: acl.related_classroom,
}
