from typing import Annotated
from typing import List
from psycopg import Cursor
from social_media_fastapi.schemas import PostSchema, PostResponseSchema


def get_all_posts(*, cursor: Cursor) -> List[PostResponseSchema]:
    cursor.execute("""
        SELECT
            *
        FROM
            public.posts;
    """)

    return [PostResponseSchema.model_validate(row) for row in cursor.fetchall()]


def get_post_by_id(*, cursor: Cursor, id: int) -> PostResponseSchema:
    cursor.execute("""
        SELECT
            *
        FROM
            public.posts
        WHERE
            id = %s;
    """, (id,))

    row = cursor.fetchone()

    if row is None:
        return None

    return PostResponseSchema.model_validate(row)


def create_post(*, cursor: Cursor, post: PostSchema) -> PostResponseSchema | None:
    cursor.execute("""
        INSERT INTO
            public.posts
            (title, content, is_published)
        VALUES
            (%s, %s, %s)
        RETURNING
            id, title, content, is_published, created_at;
    """, (post.title, post.content, post.is_published))

    row = cursor.fetchone()

    if row is None:
        return None

    return PostResponseSchema.model_validate(row)


def delete_post_by_id(*, cursor: Cursor, id: int) -> Annotated[int, "Post id"]:
    cursor.execute("""
        DELETE FROM
            public.posts
        WHERE
            id = %s
        RETURNING
            id;
    """, (id,))

    row = cursor.fetchone()

    if row is None:
        return None

    return row


def update_post_by_id(*, cursor: Cursor, id: int, post: PostSchema) -> PostResponseSchema | None:
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
    """, (post.title, post.content, post.is_published, id))

    row = cursor.fetchone()

    if row is None:
        return None

    return PostResponseSchema.model_validate(row)
