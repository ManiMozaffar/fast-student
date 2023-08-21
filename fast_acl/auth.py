import json
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from fast_acl.acl.role import UserRoles
from fast_acl.exception import CredentialsException
from fast_acl.schema import TokenData, TokenSchema
from fast_acl.settings import setting
from fast_acl.types import UserId

http_bearer = HTTPBearer()


def create_access_token(data: TokenData) -> str:
    expire_timestamp = int(
        (
            datetime.now() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        ).timestamp()
    )
    token_data = TokenSchema(user_id=data.user_id, role=data.role, exp=expire_timestamp)
    encoded_jwt = jwt.encode(
        json.loads(token_data.model_dump_json()),
        setting.SECRET_KEY,
        algorithm=setting.ALGORITHM,
    )
    return encoded_jwt


def decode_jwt(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        user_id: UserId | None = payload.get("user_id")
        role: UserRoles | None = payload.get("role")
        if user_id is None or role is None:
            raise CredentialsException

        return TokenData(user_id=UserId(user_id), role=role)
    except JWTError:
        raise CredentialsException


def check_jwt(
    credentials: HTTPAuthorizationCredentials,
) -> str:
    if credentials.scheme != "Bearer":
        raise CredentialsException
    return credentials.credentials


def check_auth(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> TokenData:
    token = check_jwt(credentials)
    token_data = decode_jwt(token)
    return token_data
