from pydantic import BaseModel
from uuid import UUID
from typing import Optional  # 👈 ADD THIS

class Item(BaseModel):
    id: Optional[UUID] = None
    name: str
    price: float
    category_id: UUID