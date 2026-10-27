from os import environ

import jwt
from datetime import datetime, timezone, timedelta


class JWTService:
    _SECRET_KEY = environ['JWT_SECRET_KEY']
    _ALGORITHM = "HS256"
    _ACCESS_TOKEN_MINUTES = 20

    @classmethod
    def create_access_token(cls, *, used_id: int) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(used_id),
            "iat": now,
            "exp": now + timedelta(minutes=cls._ACCESS_TOKEN_MINUTES)
        }

        return jwt.encode(payload=payload, key=cls._SECRET_KEY, algorithm=cls._ALGORITHM)
