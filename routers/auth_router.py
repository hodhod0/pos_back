from fastapi import APIRouter
from models.user import User
import crud.auth_crud as auth_crud

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(user: User):
    return auth_crud.signup(user)

@router.post("/login")
def login(user: User):
    return auth_crud.login(user)