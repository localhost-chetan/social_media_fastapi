from social_media_fastapi.database import pool
from social_media_fastapi.schemas import UserSchema, UserResponseSchema
from fastapi import APIRouter, status, HTTPException
from social_media_fastapi.repositories import users as user_repository
from social_media_fastapi.services.hashing import PasswordHashingService


router = APIRouter(prefix="/users", tags=['users'])


@router.get("/")
def get_users():
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            all_users = user_repository.get_all_useers(cursor=cursor)
            return all_users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user(user: UserSchema):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            existing_user = user_repository.find_user_by_email(
                cursor=cursor, email=user.email)

            if existing_user is None:
                hashed_password = PasswordHashingService().hash_password(password=user.password)
                user.__dict__['password'] = hashed_password
                new_user = user_repository.create_new_user(
                    cursor=cursor, user=user)
                return new_user
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"User with email {user.email} already exists")


@router.get("/{id}", response_model=UserResponseSchema)
def get_user(id: int):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            user = user_repository.get_user_by_id(cursor=cursor, id=id)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

            return user
