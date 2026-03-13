from fastapi import APIRouter, HTTPException
from crud.set_users_crud import get_user_by_username,get_all_users

router = APIRouter(prefix="/set_users", tags=["set_users"])

@router.get("/by_username")
def read_users():
    result = get_user_by_username()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
@router.get("/")
def read_users():
    result = get_all_users()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result