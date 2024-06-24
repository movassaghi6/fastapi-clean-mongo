from pydantic import BaseModel
from typing import List, Optional, Dict, Union
from datetime import datetime
# user request
class CreateUserRequest(BaseModel):
    email: str
    password: str
    name: str



# user response
class CreateUserResponse(BaseModel):
    user_id:  str
    email: str
    name: str
    created_at: datetime


class ListUsersResponse(BaseModel):
    users: List[CreateUserResponse]
    meta: Optional[Dict[str, Union[str, int]]]

class DeleteUserResponse(BaseModel):
    user_id: str

class UpdateUserRequest(BaseModel):
    email: str
    name: str
    password: str

class UpdateUserResponse(BaseModel):
    user_id:  str
    email: str
    name: str
    created_at: datetime
