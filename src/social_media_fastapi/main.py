from fastapi import FastAPI, status, HTTPException
from psycopg import connect, OperationalError, Error as PsycopgError
from psycopg.rows import dict_row
from os import environ
from dotenv import load_dotenv
from time import sleep
from .schemas import PostBase
from .repositories import posts as posts_repository

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

        print("Connected to PostgreSQL")
        break


@app.get('/')
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    all_posts = posts_repository.get_all_posts(cursor=cursor)
    return all_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostBase):
    post = posts_repository.create_post(cursor=cursor, post=post)
    return post


@app.get("/posts/{id}")
def get_post(id: int):
    post = posts_repository.get_post_by_id(cursor=cursor, id=id)

    if not (post == None):
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = posts_repository.delete_post_by_id(cursor=cursor, id=id)

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")


@app.put("/posts/{id}")
def update_post(id: int, post: PostBase):
    post_id = posts_repository.get_post_by_id(cursor=cursor, id=id)

    if post_id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    else:
        updated_post = posts_repository.update_post_by_id(
            cursor=cursor, id=id, post=post)

        return updated_post
