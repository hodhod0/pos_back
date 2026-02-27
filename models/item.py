# models/item.py
from pydantic import BaseModel
from uuid import UUID

class Item(BaseModel):
    id: Optional[UUID] = None  # optional item ID
    name: str
    price: float
    category_id: UUID  # link to Category