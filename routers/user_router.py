from fastapi import APIRouter, HTTPException
from models.user import User
import crud.user_crud as user_crud
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def read_users():
    result = user_crud.get_all_users()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/")
def create_user(user: User):
    result = user_crud.add_user(user)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

