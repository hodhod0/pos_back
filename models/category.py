# models/category.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4

class Category(BaseModel):
    id: Optional[UUID] = None  # UUID primary key
    name: str