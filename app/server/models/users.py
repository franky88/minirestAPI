from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUserRequest(BaseModel):
    name: str or None = None
    username: str
    password: str
    email: EmailStr
    is_admin: bool = False
    is_active: bool = True

class UpdateUserRequest(BaseModel):
    name: Optional[str]
    email: Optional[str]
    is_admin: bool = False
    is_active: bool = True