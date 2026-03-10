from uuid import uuid4
from db import get_connection
from models.user import User
from utils.auth import create_access_token  # we can still use JWT

def signup(user: User):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        user_id = str(user.id or uuid4())

        cursor.execute(
            """
            INSERT INTO users (id, username, password, full_name, role_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, user.username, user.password, user.full_name, str(user.role_id), int(user.is_active))
        )

        conn.commit()
        return {"message": "User created successfully", "user_id": user_id}

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()


def login(user):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username = %s",
            (user.username,)
        )
        row = cursor.fetchone()

        if row and user.password == row[0]:
            token = create_access_token({"sub": user.username})
            return {"access_token": token, "token_type": "bearer"}

        return {"error": "Invalid username or password"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()