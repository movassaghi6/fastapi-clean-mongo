from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from app.model.user import PyObjectId


# user request
class CreateUserRequest(BaseModel):
    email: str
    password: str
    name: str

# user response
class CreateUserResponse(BaseModel):
    user_id:  str
    email: EmailStr
    name: str
    created_at: datetime

