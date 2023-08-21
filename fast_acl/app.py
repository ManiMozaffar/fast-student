from typing import Callable

import uvicorn
from fastapi import Depends, FastAPI

from fast_acl.acl.mapper import (
    PermissionGrants,
    UserRoles,
    get_permission_callable,
    get_permission_setting,
)
from fast_acl.acl.routes import RoutesEnum
from fast_acl.auth import TokenData, check_auth, create_access_token
from fast_acl.schema import ProtectedMessage, Token

app = FastAPI()


@app.post("/token", response_model=Token)
async def login_for_access_token(payload: TokenData):
    access_token = create_access_token(data=payload)
    return {"access_token": access_token}


@app.get(
    "/protected-route",
    dependencies=[Depends(check_auth)],
    response_model=ProtectedMessage,
)
async def read_protected_route():
    return ProtectedMessage(message="You have access to this protected route!")


@app.post("classroom/{classroom_id}/student")
async def create_student(
    token: TokenData = Depends(check_auth),
    permission_callable: Callable = Depends(get_permission_callable),
    permission_setting: dict[RoutesEnum, dict[UserRoles, PermissionGrants]] = Depends(
        get_permission_setting
    ),
):
    await permission_callable(
        user_rule=token.role,
        user_id=token.user_id,
        route=RoutesEnum.ADD_STUDENT,
        permission_setting=permission_setting,
    )


@app.get("classroom/{classroom_id}/student/{student_id}")
async def get_student(
    permission_callable: Callable = Depends(get_permission_callable),
):
    route_enum = RoutesEnum.READ_STUDENT


@app.put("classroom/{classroom_id}/student/{student_id}")
async def update_student(
    permission_callable: Callable = Depends(get_permission_callable),
):
    route_enum = RoutesEnum.UPDATE_STUDENT


@app.delete("classroom/{classroom_id}/student/{student_id}")
async def delete_student(
    permission_callable: Callable = Depends(get_permission_callable),
):
    route_enum = RoutesEnum.DELETE_STUDENT


@app.patch("classroom/{classroom_id}/student/{student_id}")
async def expel_student(
    permission_callable: Callable = Depends(get_permission_callable),
):
    route_enum = RoutesEnum.EXPEL_STUDENT


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
