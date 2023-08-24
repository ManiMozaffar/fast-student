from fast_acl.acl.grants import PermissionGrants
from fast_acl.acl.role import UserRoles
from fast_acl.acl.routes import RoutesEnum


def mock_permission_setting():
    ACL_MAPPER: dict[RoutesEnum, dict[UserRoles, PermissionGrants]] = {}
    for router in RoutesEnum:
        ACL_MAPPER[router] = {}
        for role in UserRoles:
            ACL_MAPPER[router][role] = PermissionGrants.IS_ALLOWED
    return ACL_MAPPER
