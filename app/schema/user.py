from pydantic import BaseModel
from typing import List, Optional, Dict, Union
from datetime import datetime


# User request schemas
class CreateUserRequest(BaseModel):
    """
    Schema for creating a new user.
    """
    email: str
    password: str
    username: str


class User(BaseModel):
    """
    Schema for representing a user.
    """
    user_id:  str
    email: str | None = None
    username: str
    created_at: datetime


class UserInDB(User):
    """
    Schema for representing a user stored in the database, extending the base User schema.
    """
    hashed_password: str


class ListUsersResponse(BaseModel):
    """
    Response schema for listing multiple users.

    Attributes:
        users (List[User]): A list of User objects.
        meta (Optional[Dict[str, Union[str, int]]]): Additional metadata, like pagination info.
    """
    users: List[User]
    meta: Optional[Dict[str, Union[str, int]]]

class DeleteUserResponse(BaseModel):
    """
    Response schema for deleting a user.
    """
    user_id: str

class UpdateUserRequest(BaseModel):
    """
    Request schema for updating a user's details.
    """
    email: str | None = None
    name: str | None = None
    password: str | None = None

class UpdateUserResponse(BaseModel):
    """
    Response schema for a successful user update.
    """
    email: str
    name: str
    created_at: datetime


class Token(BaseModel):
    """
    Schema for an access token.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (typically 'Bearer').
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data, typically used when extracting information from a token.

    Attributes:
        username (Optional[str]): The username extracted from the token.
    """
    username: str | None = None
