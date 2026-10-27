from ..database import pool
from social_media_fastapi.schemas import UserBase, UserOut
from fastapi import APIRouter, status, HTTPException
from social_media_fastapi.repositories import users as users_repository


router = APIRouter(prefix="/users", tags=['users'])


@router.get("/")
def get_users():
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            all_users = users_repository.get_all_useers(cursor=cursor)
            return all_users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserBase):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            existing_user = users_repository.find_user_by_email(
                cursor=cursor, email=user.email)

            if existing_user is None:
                new_user = users_repository.create_new_user(
                    cursor=cursor, user=user)
                return new_user
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"User with email {user.email} already exists")
