from models.set_users import SetUser, LoginModel
from crud.set_users_crud import add_user, get_user_by_username
from utils.auth import create_access_token, verify_password

# Signup
def signup(user: SetUser):
    print("Signup payload:", user.dict())
    existing = get_user_by_username(user.usr_username)
    if existing:
        return {"error": "Username already exists"}
    return add_user(user)

# Login
def login(user: LoginModel):
    print("Login payload received:", user.dict())
    db_user = get_user_by_username(user.usr_username)
    if not db_user:
        return {"error": "Invalid username or password"}

    print("Submitted password:", user.usr_password)
    print("DB password:", db_user["usr_password"])

    if not verify_password(user.usr_password, db_user["usr_password"]):
        return {"error": "Invalid username or password"}

    token = create_access_token({
        "sub": db_user["usr_username"],
        "usr_id": str(db_user["usr_id"]),
        "usr_role_id": str(db_user["usr_role_id"])
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "usr_id": str(db_user["usr_id"]),
            "usr_name": db_user["usr_name"],
            "usr_username": db_user["usr_username"],
            "usr_role_id": str(db_user["usr_role_id"]),
            "usr_active": bool(db_user["usr_active"]),
            "sys_name": db_user["sys_name"] 
        }
    }