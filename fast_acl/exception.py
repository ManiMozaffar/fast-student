from uuid import UUID

from fastapi import HTTPException, status


class BaseCustomException(Exception):
    ...


class NotFoundError(BaseCustomException):
    def __init__(self, obj_id: str | UUID) -> None:
        self.obj_id = obj_id
        super().__init__(f"Object with ID {obj_id} was not found")


class NotAuthorizedError(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not authenicate user",
        )


class CredentialsException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
