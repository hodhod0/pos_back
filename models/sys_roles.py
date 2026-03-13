from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class RoleBase(BaseModel):
    sys_name: str
    sys_description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    sys_id: UUID