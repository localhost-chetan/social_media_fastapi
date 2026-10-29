from typing import Literal, Annotated
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


Password = Annotated[str, Field(..., min_length=3,

                                description="Password must contain uppercase, lowercase, digits, and special symbols(@#$-_)",
                                examples=["Password_9856"])]

# Post Schema


class PostSchema(BaseModel):
    """ This model describes the data you API accepts from client. """
    title: str
    content: str
    is_published: bool = True


class PostResponseSchema(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    created_at: datetime


# User Schema

class UserSchema(BaseModel):
    """ Validate user registration input, including email and password. """
    email: EmailStr
    password: Password


class UserResponseSchema(BaseModel):
    """ Represent public user data returned by the API, excluding the password. """
    id: int
    email: EmailStr
    created_at: datetime


# Internal Model used when authenticate needs the stored hash
class UserWithPasswordSchema(UserResponseSchema):
    password: Password


# Response sent after successful login
class LoginResponseSchema(BaseModel):
    access_token: str
    type: Literal["bearer"] = "bearer"
