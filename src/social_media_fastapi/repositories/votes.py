from psycopg import Cursor
from social_media_fastapi.schemas import VoteResponseSchema


def get_post_vote(*, cursor: Cursor, post_id: int, user_id: int):
    cursor.execute("""
        SELECT
            *
        FROM
            public.votes
        WHERE
            post_id = %s
                AND
            user_id = %s;
    """, (post_id, user_id))

    row = cursor.fetchone()

    return row


def create_vote(*, cursor: Cursor, post_id: int, user_id: int) -> VoteResponseSchema:
    cursor.execute("""
        INSERT INTO public.votes
            (post_id, user_id)
        VALUES
            (%s, %s)
        RETURNING
            post_id, user_id;
    """, (post_id, user_id))

    row = cursor.fetchone()

    if row is None:
        return None

    return VoteResponseSchema.model_validate(row)


def delete_vote(*, cursor: Cursor, post_id: int, user_id: int):
    cursor.execute("""
        DELETE FROM
            public.votes
        WHERE
            post_id = %s
                AND 
            user_id = %s
        RETURNING
            *;
    """, (post_id, user_id))

    row = cursor.fetchone()

    return row
