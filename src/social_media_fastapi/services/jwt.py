from typing import Literal
from social_media_fastapi.utils import get_env_key

import jwt
from typing import Any
from datetime import datetime, timezone, timedelta


KeyType = Literal["JWT_SECRET_KEY", "JWT_EXPIRATION_TIME"]


class JWTService:
    __ALGORITHM = "HS256"

    @classmethod
    def create_access_token(cls, *, user_id: int) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=float(get_env_key(key_name="JWT_EXPIRATION_TIME")))
        }

        return jwt.encode(payload=payload, key=get_env_key(key_name="JWT_SECRET_KEY"), algorithm=cls.__ALGORITHM)

    @classmethod
    def decode_access_token(cls, *, token: str) -> dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=get_env_key(key_name="JWT_SECRET_KEY"),
            algorithms=[cls.__ALGORITHM]
        )
