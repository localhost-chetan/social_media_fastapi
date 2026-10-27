from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    """ This model describes the data you API accepts from client. """
    title: str
    content: str
    is_published: bool = True


class UserBase(BaseModel):
    """ Validate user registration input, including email and password. """
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """ Represent public user data returned by the API, excluding the password. """
    id: int
    email: EmailStr
    created_at: datetime

    class WithPassword:
        password: str


class Login(BaseModel):
    access_token: str
    type: str
