from os import environ
from typing import Literal
from dotenv import load_dotenv

load_dotenv()


KeyType = Literal["JWT_SECRET_KEY",
                  "JWT_EXPIRATION_TIME", "DATABASE_URL", "APP_ENV"]


def get_env_key(*, key_name: KeyType):
    secret_key = environ.get(key_name)

    if secret_key is None:
        raise KeyError(
            f'Missing required environment variable: "{key_name}"')
    return secret_key
