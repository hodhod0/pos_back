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
            SELECT 
                usr_id,
                usr_name,
                usr_username,
                usr_role_id,
                usr_active,
                usr_created_at
            FROM set_users
        """)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    except Exception as e:
        print("❌ DB Error in get_all_users():", e)
        return {"error": str(e)}

    finally:
        conn.close()


# Add a new user
def add_user(user):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        hashed_pwd = hash_password(user.usr_password)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO set_users 
                (usr_name, usr_username, usr_password, usr_role_id, usr_active)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            user.usr_name,
            user.usr_username,
            hashed_pwd,
            user.usr_role_id,
            int(user.usr_active)
        ))

        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()

        return {
            "usr_id": new_id,
            "usr_name": user.usr_name,
            "usr_username": user.usr_username,
            "usr_role_id": user.usr_role_id,
            "usr_active": user.usr_active
        }

    except Exception as e:
        print("❌ DB Error in add_user():", e)
        return {"error": str(e)}

    finally:
        conn.close()


# Get user by ID
def get_user_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            u.usr_id,
            u.usr_name,
            u.usr_username,
            u.usr_password,
            u.usr_role_id,
            u.usr_active,
            r.sys_name
        FROM set_users u
        LEFT JOIN sys_roles r 
            ON r.sys_id = u.usr_role_id
        WHERE u.usr_username = %s
    """

    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
# Update user
def update_user(user_id, user):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor()
        query = """
            UPDATE set_users 
            SET usr_name=%s,
                usr_username=%s,
                usr_role_id=%s,
                usr_active=%s
        """
        params = [
            user.usr_name,
            user.usr_username,
            user.usr_role_id,
            int(user.usr_active)
        ]

        # Update password only if provided
        if hasattr(user, "usr_password") and user.usr_password:
            hashed_pwd = hash_password(user.usr_password)
            query += ", usr_password=%s"
            params.append(hashed_pwd)

        query += " WHERE usr_id=%s"
        params.append(user_id)

        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()

        return {"success": True}

    except Exception as e:
        print("❌ DB Error in update_user():", e)
        return {"error": str(e)}

    finally:
        conn.close()


# Delete user
def delete_user(user_id):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM set_users WHERE usr_id=%s;", (user_id,))
        conn.commit()
        cursor.close()
        return {"success": True}

    except Exception as e:
        print("❌ DB Error in delete_user():", e)
        return {"error": str(e)}

    finally:
        conn.close()