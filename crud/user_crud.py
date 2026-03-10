from uuid import uuid4
from db import get_connection
from utils.auth import hash_password

# Get all users
def get_all_users():
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * 
            FROM users;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ DB Error in get_all_users():", e)
        return {"error": str(e)}

# Add a new user
def add_user(user):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        user_id = str(uuid4())
        hashed_pwd = hash_password(user.password)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (id, username, password_hash, full_name, role_id, is_active) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, user.username, hashed_pwd, user.full_name, str(user.role_id), user.is_active)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "id": user_id,
            "username": user.username,
            "full_name": user.full_name,
            "role_id": user.role_id,
            "is_active": user.is_active
        }
    except Exception as e:
        print("❌ DB Error in add_user():", e)
        return {"error": str(e)}

# Get user by ID
def get_user_by_id(user_id):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, full_name, role_id, is_active 
            FROM users WHERE id=%s;
        """, (str(user_id),))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return row
        return {"error": "User not found"}
    except Exception as e:
        print("❌ DB Error in get_user_by_id():", e)
        return {"error": str(e)}

# Update user
def update_user(user_id, user):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor()
        query = "UPDATE users SET username=%s, full_name=%s, role_id=%s, is_active=%s"
        params = [user.username, user.full_name, str(user.role_id), user.is_active]
        if hasattr(user, "password") and user.password:
            hashed_pwd = hash_password(user.password)
            query += ", password_hash=%s"
            params.append(hashed_pwd)
        query += " WHERE id=%s"
        params.append(str(user_id))
        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        print("❌ DB Error in update_user():", e)
        return {"error": str(e)}

# Delete user
def delete_user(user_id):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s;", (str(user_id),))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        print("❌ DB Error in delete_user():", e)
        return {"error": str(e)}