from datetime import datetime, timedelta
from jose import jwt

# Dummy password functions
def hash_password(password: str) -> str:
    return password

def verify_password(password: str, hashed: str) -> bool:
    return password == hashed

# JWT config
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)