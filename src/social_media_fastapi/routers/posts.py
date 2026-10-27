from social_media_fastapi.database import pool
from social_media_fastapi.schemas import PostBase
from fastapi import APIRouter, HTTPException, status
from social_media_fastapi.repositories import posts as posts_repository


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
def get_posts():
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            all_posts = posts_repository.get_all_posts(cursor=cursor)
            return all_posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostBase):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            created_post = posts_repository.create_post(
                cursor=cursor, post=post)
            return created_post


@router.get("/{id}")
def get_post(id: int):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            post = posts_repository.get_post_by_id(cursor=cursor, id=id)

            if not (post == None):
                return post
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            deleted_post = posts_repository.delete_post_by_id(
                cursor=cursor, id=id)

            if deleted_post == None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


@router.put("/{id}")
def update_post(id: int, post: PostBase):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            post_id = posts_repository.get_post_by_id(cursor=cursor, id=id)

            if post_id == None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

            else:
                updated_post = posts_repository.update_post_by_id(
                    cursor=cursor, id=id, post=post)

                return updated_post
