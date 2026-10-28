from typing import Any
from psycopg import Cursor
from social_media_fastapi.schemas import UserSchema, UserResponseSchema


def get_all_useers(*, cursor: Cursor):
    cursor.execute("""
        SELECT
            id, email, created_at
        FROM
            public.users;
    """)

    return cursor.fetchall()


def create_new_user(*, cursor: Cursor, user: UserSchema):
    cursor.execute("""
        INSERT INTO
            public.users
            (email, password)
        VALUES
            (%s, %s)
        RETURNING
            id, email, created_at;
    """, (user.email, user.password))

    return cursor.fetchone()


def find_user_by_email(*, cursor: Cursor, email: str) -> UserResponseSchema.WithPassword:
    cursor.execute("""
        SELECT
            id, email, password
        FROM
            public.users
        WHERE
            email = %s
    """, (email, ))

    return cursor.fetchone()


def get_user_by_id(*, cursor: Cursor, id: int):
    cursor.execute("""
        SELECT
            id, email, created_at
        FROM
            public.users
        WHERE
            id = %s
    """, (str(id), ))

    return cursor.fetchone()


def get_user_password(*, cursor: Cursor, password: str):
    cursor.execute("""
        SELECT
            password
        FROM
            public.users
        WHERE
            password = %s
    """, (password, ))

    return cursor.fetchone()
