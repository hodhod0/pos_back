from fastapi import APIRouter, HTTPException
from models.set_users import SetUser, LoginModel
from services.auth_service import signup, login

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def register(user: SetUser):
    result = signup(user)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/login")
def user_login(user: LoginModel):
    result = login(user)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result