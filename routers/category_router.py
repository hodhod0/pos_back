from fastapi import APIRouter
from models.category import Category
import crud.category_crud as category_crud

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/")
def read_categories():
    return category_crud.get_all_categories()

@router.post("/")
def create_category(category: Category):
    return category_crud.add_category(category)

@router.delete("/{cat_id}")
def delete_category(cat_id: str):
    result = category_crud.delete_category(cat_id)
    return result

