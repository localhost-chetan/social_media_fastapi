from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostSchema(BaseModel):
    """ This model describes the data you API accepts from client. """
    title: str
    content: str
    is_published: bool = True


class UserSchema(BaseModel):
    """ Validate user registration input, including email and password. """
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    """ Represent public user data returned by the API, excluding the password. """
    id: int
    email: EmailStr
    created_at: datetime

    class WithPassword:
        password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    type: str
