from typing import Annotated
from jwt import InvalidTokenError
from psycopg_pool import ConnectionPool
from social_media_fastapi.database import pool
from fastapi import Depends, HTTPException, status
from social_media_fastapi.services.jwt import JWTService
from social_media_fastapi.schemas import UserResponseSchema
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from social_media_fastapi.repositories import users as user_repository


def get_db_pool() -> ConnectionPool:
    """ Return the existing pool, not a newly created pool """
    return pool


DbPool = Annotated[ConnectionPool, Depends(get_db_pool)]


# Extract a bearer token from the Authorization header
_bearer_scheme = HTTPBearer(auto_error=False)


def _credentials_error() -> HTTPException:
    """ It prepares an error response for failed authentication """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentails",
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_current_user(
    *,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)],
    db_pool: DbPool
):
    if credentials is None:
        raise _credentials_error()

    token = credentials.credentials

    try:
        payload = JWTService().decode_access_token(token=token)

        subject = payload.get("sub")

        if not isinstance(subject, str):
            raise ValueError("Invalid token subject")

        user_id = int(subject)
    except (InvalidTokenError, ValueError, TypeError) as error:
        raise _credentials_error() from None

    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            user = user_repository.get_user_by_id(cursor=cursor, id=user_id)

    if user is None:
        raise _credentials_error()

    return user


# Use this annotation in routes that require an authenticated user
CurrentUser = Annotated[
    UserResponseSchema,
    Depends(get_current_user)
]
