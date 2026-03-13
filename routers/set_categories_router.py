from fastapi import APIRouter
from models.set_categories import Category
import crud.set_categories_crud as set_categories_crud

router = APIRouter(prefix="/set_categories", tags=["set_categories"])

@router.get("/")
def read_categories():
    return set_categories_crud.get_all_categories()

@router.post("/")
def create_category(category: Category):
    return set_categories_crud.add_category(category)

@router.delete("/{cat_id}")
def delete_category(cat_id: str):
    result = set_categories_crud.delete_category(cat_id)
    return result

@router.put("/{cat_id}")
def update_category(cat_id: str, category: Category):
    result = set_categories_crud.update_category(cat_id, category)
    return result