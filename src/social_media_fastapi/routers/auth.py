from social_media_fastapi.services.jwt import JWTService
from social_media_fastapi.services.hashing import verify_password
from fastapi import APIRouter, HTTPException, status
from social_media_fastapi.database import pool
from social_media_fastapi.schemas import UserBase, Login
from social_media_fastapi.repositories import users as user_repository


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Login)
def login(user_credentials: UserBase):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            existing_user = user_repository.find_user_by_email(
                cursor=cursor, email=user_credentials.email)

            if existing_user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with email {user_credentials.email} not found")

            is_password_valid = verify_password(
                password=user_credentials.password, hashed_password=existing_user['password'])

            if not is_password_valid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")

            # create access token (JWT)
            jwt = JWTService().create_access_token(user_id=existing_user['id'])

            return {
                "access_token": jwt,
                "type": "bearer"
            }
