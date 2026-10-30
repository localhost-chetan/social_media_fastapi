from social_media_fastapi.dependencies import DbPool
from social_media_fastapi.schemas import UserSchema, UserResponseSchema
from fastapi import APIRouter, status, HTTPException
from social_media_fastapi.repositories import users as user_repository
from social_media_fastapi.services.hashing import PasswordHashingService


router = APIRouter(prefix="/users", tags=['users'])


@router.get("/")
def get_users(db_pool: DbPool):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            all_users = user_repository.get_all_users(cursor=cursor)
            return all_users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user(user: UserSchema, db_pool: DbPool):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            hashed_password = PasswordHashingService().hash_password(password=user.password)
            user.password = hashed_password
            new_user = user_repository.create_user(
                cursor=cursor, user=user)

            if new_user is None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"User with email {user.email} already exists")
            return new_user


@router.get("/{id}", response_model=UserResponseSchema)
def get_user(id: int, db_pool: DbPool):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            user = user_repository.get_user_by_id(cursor=cursor, id=id)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

            return user
