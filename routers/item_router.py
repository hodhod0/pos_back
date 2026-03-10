from fastapi import APIRouter, HTTPException
from uuid import UUID
from pydantic import BaseModel
import crud.item_crud as item_crud
from models.item import Item  # Your original Item model for POST.

router = APIRouter(prefix="/items", tags=["Items"])


# --------------------------
# Pydantic model for updates
# --------------------------
class ItemPayload(BaseModel):
    name: str
    price: float
    category_id: UUID | None = None


# --------------------------
# GET all items
# --------------------------
@router.get("/")
def read_items():
    result = item_crud.get_all_items()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# --------------------------
# CREATE item
# --------------------------
@router.post("/")
def create_item(item: Item):
    result = item_crud.add_item(item)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# --------------------------
# GET items by category
# --------------------------
@router.get("/category/{category_id}")
def read_items_by_category(category_id: UUID):
    result = item_crud.get_items_by_category(category_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# --------------------------
# DELETE item
# --------------------------
@router.delete("/{item_id}")
async def api_delete_item(item_id: UUID):
    result = item_crud.delete_item(item_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# --------------------------
# UPDATE item
# --------------------------
@router.put("/edit/{item_id}")
async def api_update_item(item_id: UUID, payload: ItemPayload):
    """
    Update an existing item by ID.
    """
    # Construct item object to pass to CRUD
    item_obj = {
        "id": item_id,
        "name": payload.name,
        "price": payload.price,
        "category_id": payload.category_id,
    }

    result = item_crud.update_item(item_obj)

    # Handle not found
    if "error" in result and "not found" in result["error"].lower():
        raise HTTPException(status_code=404, detail=result["error"])

    # Handle other possible errors
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {"message": "Item updated successfully", "item": item_obj}