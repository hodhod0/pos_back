from fastapi import APIRouter
from models.user import User, LoginModel
from services.auth_service import signup, login


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def register(user: User):
    return signup(user)

@router.post("/login")
def user_login(user: LoginModel):
    return login(user)