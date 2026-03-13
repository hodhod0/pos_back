from pydantic import BaseModel
from typing import Optional

# User model for signup and DB
class SetUser(BaseModel):
    usr_id: Optional[int] = None
    usr_name: str
    usr_username: str
    usr_password: str
    usr_role_id: int
    usr_active: Optional[bool] = True

# Login model
class LoginModel(BaseModel):
    usr_username: str
    usr_password: str