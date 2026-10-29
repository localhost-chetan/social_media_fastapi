from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


Password = Annotated[str, Field(...,
                                min_length=3,
                                description="Password must contain uppercase, lowercase, digits, and special symbols(@#$-_)",
                                examples=["Password_9856"])
                     ]

# Post Schema


class PostSchema(BaseModel):
    """Validate the fields a client may provide when creating or updating a post.

    The title and content are supplied by the client. ``is_published`` defaults
    to ``True`` when omitted.
    """
    title: str
    content: str
    is_published: bool = True
    user_id: int


class PostResponseSchema(BaseModel):
    """Represent a post returned by the API after it has been persisted.

    Includes the database-generated post ID and creation timestamp alongside
    the post content and publication state.
    """
    id: int
    title: str
    content: str
    is_published: bool
    created_at: datetime
    user_id: int


# User Schema

class UserSchema(BaseModel):
    """Validate credentials submitted by a client during registration or login.

    The email is validated as an email address, and the password uses the
    shared ``Password`` type's declared constraints.
    """
    email: EmailStr
    password: Password


class UserResponseSchema(BaseModel):
    """Represent public user information returned by the API.

    Contains the user's database ID, validated email address, and creation
    timestamp. Passwords and password hashes are intentionally excluded.
    """
    id: int
    email: EmailStr
    created_at: datetime


# Internal Model used when authenticate needs the stored hash
class UserWithPasswordSchema(UserResponseSchema):
    """Represent a user record loaded for authentication.

    Extends the public user fields with the password value read from storage.
    This internal model should not be used as an API response, since it
    contains sensitive authentication data.
    """
    password: Password


# Response sent after successful login
class LoginResponseSchema(BaseModel):
    """Describe the successful login response returned to a client.

    ``message`` carries the response message and ``token`` carries the
    credential used to authenticate subsequent requests.
    """
    message: str
    token: str
