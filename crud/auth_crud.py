from uuid import uuid4
from db import get_connection
from models.set_users import SetUser
from utils.auth import hash_password, verify_password, create_access_token

def signup(user: SetUser):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        hashed = hash_password(user.password)
        user_id = str(user.usr_id or uuid4())

        cursor.execute(
            """
            INSERT INTO set_users (usr_id, username, password, full_name, role_id, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, user.username, hashed, user.full_name, str(user.role_id), int(user.is_active))
        )

        conn.commit()
        return {"message": "User created successfully", "user_id": user_id}

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()
        
        


def login(user: SetUser):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT usr_id, username, password, full_name, role_id, is_active
            FROM set_users
            WHERE username = ?
            """,
            (user.username,)
        )

        row = cursor.fetchone()

        if not row:
            return {"error": "Invalid username or password"}

        db_id, db_username, db_password, full_name, role_id, is_active = row

        # verify password
        if not verify_password(user.password, db_password):
            return {"error": "Invalid username or password"}

        # create JWT token
        token = create_access_token({
            "sub": db_username,
            "user_id": db_id,
            "role_id": role_id
        })

        # ✅ return user info
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "usr_id": db_id,
                "username": db_username,
                "full_name": full_name,
                "role_id": role_id,
                "is_active": bool(is_active)
            }
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()
        
        