from os import environ

import jwt
from datetime import datetime, timezone, timedelta


class JWTService:
    __ALGORITHM = "HS256"
    __ACCESS_TOKEN_MINUTES = 20

    @staticmethod
    def __get_secret_key() -> str:
        secret_key = environ.get('JWT_SECRET_KEY')

        if secret_key is None:
            raise KeyError(
                'Missing required environment variable: "JWT_SECRET_KEY"')
        return secret_key

    @classmethod
    def create_access_token(cls, *, user_id: int) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=cls.__ACCESS_TOKEN_MINUTES)
        }

        return jwt.encode(payload=payload, key=cls.__get_secret_key(), algorithm=cls.__ALGORITHM)
