from psycopg import Cursor
from social_media_fastapi.schemas import PostBase


def get_all_posts(*, cursor: Cursor):
    cursor.execute("""
        SELECT
            *
        FROM
            public.posts;
    """)

    return cursor.fetchall()


def get_post_by_id(*, cursor: Cursor, id: int):
    cursor.execute("""
        SELECT
            *
        FROM
            public.posts
        WHERE
            id = %s;
    """, (str(id),))

    return cursor.fetchone()


def create_post(*, cursor: Cursor, post: PostBase):
    cursor.execute("""
        INSERT INTO
            public.posts
            (title, content, is_published)
        VALUES
            (%s, %s, %s)
        RETURNING
            title, content, is_published;
    """, (post.title, post.content, post.is_published))

    return cursor.fetchone()


def delete_post_by_id(*, cursor: Cursor, id: int):
    cursor.execute("""
        DELETE FROM
            public.posts
        WHERE
            id = %s
        RETURNING
            id;
    """, (str(id),))

    return cursor.fetchone()


def update_post_by_id(*, cursor: Cursor, id: int, post: PostBase):
    cursor.execute("""
        UPDATE
            public.posts
        SET
            title = %s,
            content = %s,
            is_published = %s
        WHERE
            id = %s
        RETURNING
            *;
    """, (post.title, post.content, post.is_published, str(id)))

    return cursor.fetchone()
