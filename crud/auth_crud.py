from db import get_connection
from models.user import User
from utils.auth import hash_password, verify_password, create_access_token

def signup(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(user.password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", user.username, hashed)
    conn.commit()
    conn.close()
    return {"message": "User created successfully"}

def login(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM user WHERE username = ?", user.username)
    row = cursor.fetchone()
    conn.close()
    if row and verify_password(user.password, row[0]):
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}