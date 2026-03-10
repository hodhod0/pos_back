from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class User(BaseModel):
    id: Optional[UUID] = None
    username: str
    password: str
    full_name: str
    role_id: UUID
    is_active: Optional[bool] = True

class LoginModel(BaseModel):
    username: str
    password: str