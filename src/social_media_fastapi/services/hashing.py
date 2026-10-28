from pwdlib import PasswordHash


class PasswordHashingService:
    __hasher = PasswordHash.recommended()

    @classmethod
    def hash_password(cls, *, password: str) -> str:
        return cls.__hasher.hash(password)

    @classmethod
    def verify_password(cls, *, password: str, hashed_password: str) -> bool:
        return cls.__hasher.verify(password=password, hash=hashed_password)
