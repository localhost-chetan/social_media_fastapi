from social_media_fastapi.dependencies import CurrentUser, DbPool
from social_media_fastapi.services.jwt import JWTService
from social_media_fastapi.services.hashing import PasswordHashingService
from fastapi import APIRouter, HTTPException, status, Response
from social_media_fastapi.schemas import UserSchema, LoginResponseSchema, UserResponseSchema
from social_media_fastapi.repositories import users as user_repository
from social_media_fastapi.utils import get_env_key


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponseSchema)
def login(user_credentials: UserSchema, db_pool: DbPool, response: Response):
    with db_pool.connection() as connection:
        with connection.cursor() as cursor:
            existing_user = user_repository.get_user_for_authentication(
                cursor=cursor, email=user_credentials.email)

            if existing_user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with email {user_credentials.email} not found")

            is_password_valid = PasswordHashingService().verify_password(
                password=user_credentials.password, hashed_password=existing_user.password)

            if not is_password_valid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")

            # create access token (JWT)
            try:
                jwt = JWTService().create_access_token(
                    user_id=existing_user.id)
            except KeyError as error:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{error}")

            is_production = get_env_key(key_name="APP_ENV") == 'production'
            jwt_expiration_time = float(get_env_key(
                key_name="JWT_EXPIRATION_TIME")) * 60

            response.set_cookie(
                key="access_token",
                value=jwt,
                httponly=True,
                secure=is_production,
                samesite="lax",
                max_age=jwt_expiration_time,  # minutes
                path="/"
            )

            return LoginResponseSchema(message="Login successful", token=jwt)


@router.get("/me", response_model=UserResponseSchema)
def me(current_user: CurrentUser):
    return current_user
