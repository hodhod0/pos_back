# models/category.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Category(BaseModel):
    cat_id: Optional[UUID] = None
    cat_name: str