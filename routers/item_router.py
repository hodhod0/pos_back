# routers/item_router.py
from fastapi import APIRouter, HTTPException
from models.item import Item
import crud.item_crud as item_crud
from uuid import UUID

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/")
def read_items():
    result = item_crud.get_all_items()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/")
def create_item(item: Item):
    result = item_crud.add_item(item)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/category/{category_id}")
def read_items_by_category(category_id: UUID):
    result = item_crud.get_items_by_category(category_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result