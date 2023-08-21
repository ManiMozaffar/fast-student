from fastapi import HTTPException


class BaseCustomException(Exception):
    ...


class NotFoundError(BaseCustomException):
    def __init__(self, obj_id: str) -> None:
        super().__init__(f"Object with ID {obj_id} was not found")


class NotAuthorizedError(BaseCustomException):
    def __init__(self, obj_id: str) -> None:
        super().__init__(f"Object with ID {obj_id} was not found")


class CredentialsException(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=401, detail="Could not validate credentials")
