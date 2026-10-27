from psycopg import Cursor
from social_media_fastapi.schemas import UserBase


def get_all_useers(*, cursor: Cursor):
    cursor.execute("""
        SELECT
            id, email, created_at
        FROM
            public.users;
    """)

    return cursor.fetchall()


def create_new_user(*, cursor: Cursor, user: UserBase):
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


def find_user_by_email(*, cursor: Cursor, email: str):
    cursor.execute("""
        SELECT
            (email)
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
