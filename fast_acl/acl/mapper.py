from fast_acl.types import UserId

from .grants import GRANT_MAPPER, PermissionGrants
from .role import UserRoles
from .routes import RoutesEnum

ACL_MAPPER: dict[RoutesEnum, dict[UserRoles, PermissionGrants]] = {
    RoutesEnum.ADD_STUDENT: {
        UserRoles.ADMIN: PermissionGrants.IS_ALLOWED,
        UserRoles.ADVISOR: PermissionGrants.NOT_ALLOWED,
        UserRoles.STUDENT: PermissionGrants.NOT_ALLOWED,
        UserRoles.TEACHER: PermissionGrants.RELATED_CLASSROOM,
    },
    RoutesEnum.DELETE_STUDENT: {
        UserRoles.ADMIN: PermissionGrants.IS_ALLOWED,
        UserRoles.ADVISOR: PermissionGrants.NOT_ALLOWED,
        UserRoles.STUDENT: PermissionGrants.NOT_ALLOWED,
        UserRoles.TEACHER: PermissionGrants.RELATED_CLASSROOM,
    },
    RoutesEnum.EXPEL_STUDENT: {
        UserRoles.ADMIN: PermissionGrants.IS_ALLOWED,
        UserRoles.ADVISOR: PermissionGrants.NOT_ALLOWED,
        UserRoles.STUDENT: PermissionGrants.NOT_ALLOWED,
        UserRoles.TEACHER: PermissionGrants.RELATED_CLASSROOM,
    },
    RoutesEnum.UPDATE_STUDENT: {
        UserRoles.ADMIN: PermissionGrants.IS_ALLOWED,
        UserRoles.ADVISOR: PermissionGrants.NOT_ALLOWED,
        UserRoles.STUDENT: PermissionGrants.NOT_ALLOWED,
        UserRoles.TEACHER: PermissionGrants.RELATED_CLASSROOM,
    },
    RoutesEnum.READ_STUDENT: {
        UserRoles.ADMIN: PermissionGrants.IS_ALLOWED,
        UserRoles.ADVISOR: PermissionGrants.IS_ALLOWED,
        UserRoles.STUDENT: PermissionGrants.RELATED_CLASSROOM,
        UserRoles.TEACHER: PermissionGrants.RELATED_CLASSROOM,
    },
}


def get_permission_setting():
    return ACL_MAPPER


async def check_permission(
    user_rule: UserRoles,
    user_id: UserId,
    route: RoutesEnum,
    permission_setting: dict[RoutesEnum, dict[UserRoles, PermissionGrants]],
    **kwargs,
):
    permission_for_endpoint = permission_setting.get(route)
    assert permission_for_endpoint is not None
    _permission_grant = permission_for_endpoint.get(user_rule)
    permission_grant = _permission_grant or PermissionGrants.NOT_ALLOWED
    permission_func = GRANT_MAPPER.get(permission_grant)
    assert permission_func is not None
    permission_func(user_id, **kwargs)


async def get_permission_callable():
    return check_permission
