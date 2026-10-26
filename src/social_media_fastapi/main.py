from fastapi import FastAPI, status, HTTPException
from psycopg import connect, OperationalError, Error as PsycopgError
from psycopg.rows import dict_row
from os import environ
from dotenv import load_dotenv
from time import sleep
from .schemas import PostBase

load_dotenv()


app = FastAPI()


while True:
    try:
        connection = connect(
            host=environ['POSTGRES_HOST'],
            port=environ['POSTGRES_PORT'],
            dbname=environ['POSTGRES_DB'],
            user=environ['POSTGRES_USER'],
            password=environ['POSTGRES_PASSWORD'],
            row_factory=dict_row,
            autocommit=True
        )

    except KeyError as error:
        raise RuntimeError(
            f"Configuration error: missing environment variable(s) {error.args}") from error
    except OperationalError as error:
        print(f"Connection or operational error: {error}")
        sleep(2)
    except PsycopgError as error:
        raise RuntimeError(f"Database error: {error}") from error
    except Exception as error:
        raise RuntimeError(
            f"Unexpected error during database startup: {error}") from error
    else:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.posts (
            id SERIAL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_published BOOLEAN NOT NULL DEFAULT TRUE,
            PRIMARY KEY(id)
        );
        """)

        print("Connected to PostgreSQL")
        break


@app.get('/')
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""
        SELECT * FROM public.posts;
    """)
    all_posts = cursor.fetchall()
    return all_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostBase):
    cursor.execute("""
        INSERT INTO public.posts (title, content, is_published)
        VALUES
            (%s, %s, %s)
        RETURNING title, content, is_published;
    """, (post.title, post.content, post.is_published))
    post = cursor.fetchone()
    return post


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""
        SELECT * FROM public.posts
        WHERE id = %s;
    """, (str(id),))
    post = cursor.fetchone()
    if not (post == None):
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""
        DELETE FROM public.posts
        WHERE id = %s
        RETURNING *;
    """, (str(id),))
    deleted_post = cursor.fetchone()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")


@app.put("/posts/{id}")
def update_post(id: int, post: PostBase):
    cursor.execute("""
        SELECT id FROM public.posts
        WHERE id = %s
    """, (str(id),))
    post_id = cursor.fetchone()
    if post_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    else:
        cursor.execute("""
            UPDATE public.posts
            SET
                title = %s,
                content = %s,
                is_published = %s
            WHERE id = %s
            RETURNING *
        """, (post.title, post.content, post.is_published, str(id)))
        updated_post = cursor.fetchone()

        return updated_post
