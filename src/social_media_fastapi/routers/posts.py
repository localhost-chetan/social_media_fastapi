from typing import List
from fastapi import Depends
from fastapi import APIRouter, HTTPException, status
from social_media_fastapi.dependencies import ensure_post_owner
from social_media_fastapi.schemas import PostSchema, PostResponseSchema
from social_media_fastapi.dependencies import DbPool, get_current_user, CurrentUser
from social_media_fastapi.repositories import posts as post_repository


# Every endpoint in this router requires authentication
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=List[PostResponseSchema])
def get_posts(db_pool: DbPool):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            all_posts = post_repository.get_all_posts(cursor=cursor)
            return all_posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
def create_posts(post: PostSchema, db_pool: DbPool, current_user: CurrentUser):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            created_post = post_repository.create_post(
                cursor=cursor, post=post, current_user_id=current_user.id)
            return created_post


@router.get("/{id}", response_model=PostResponseSchema, dependencies=[Depends(ensure_post_owner)])
def get_post(id: int, db_pool: DbPool):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            post = post_repository.get_post_by_id(cursor=cursor, id=id)

            if not (post == None):
                return post
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(ensure_post_owner)],
)
def delete_post(id: int, db_pool: DbPool):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            deleted_post = post_repository.delete_post_by_id(
                cursor=cursor, id=id)

            if deleted_post == None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


@router.put(
    "/{id}",
    response_model=PostResponseSchema,
    dependencies=[Depends(ensure_post_owner)],
)
def update_post(id: int, post: PostSchema, db_pool: DbPool):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            updated_post = post_repository.update_post_by_id(
                cursor=cursor, id=id, post=post)

            if updated_post is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

            return updated_post
