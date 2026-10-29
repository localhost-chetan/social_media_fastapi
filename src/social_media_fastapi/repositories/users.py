from psycopg import Cursor
from social_media_fastapi.schemas import (
    UserSchema, UserResponseSchema, UserWithPasswordSchema)


def get_all_users(*, cursor: Cursor) -> list[UserResponseSchema]:
    cursor.execute("""
        SELECT
            id, email, created_at
        FROM
            public.users;
    """)

    return [UserResponseSchema.model_validate(row) for row in cursor.fetchall()]


def create_user(*, cursor: Cursor, user: UserSchema) -> UserResponseSchema | None:
    cursor.execute("""
        INSERT INTO
            public.users
            (email, password)
        VALUES
            (%s, %s)
        ON CONFLICT (email)
        DO NOTHING
        RETURNING
            id, email, created_at;
    """, (user.email, user.password))

    row = cursor.fetchone()

    if row is None:
        return None

    return UserResponseSchema.model_validate(row)


def get_user_by_id(*, cursor: Cursor, id: int) -> UserResponseSchema | None:
    cursor.execute("""
        SELECT
            id, email, created_at
        FROM
            public.users
        WHERE
            id = %s
    """, (id, ))

    row = cursor.fetchone()

    if row is None:
        return None

    return UserResponseSchema.model_validate(row)


def get_user_for_authentication(*, cursor: Cursor, email: str) -> UserWithPasswordSchema | None:
    cursor.execute("""
        SELECT
            id, email, password, created_at
        FROM
            public.users
        WHERE
            email = %s;
    """, (email,))

    row = cursor.fetchone()

    if row is None:
        return None

    return UserWithPasswordSchema.model_validate(row)
