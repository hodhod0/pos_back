from uuid import uuid4
from db import get_connection

# Get all roles
def get_all_roles():
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, description, created_at FROM roles;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ DB Error in get_all_roles():", e)
        return {"error": str(e)}

# Add a new role
def add_role(role):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        role_id = str(uuid4())
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO roles (id, name, description) VALUES (%s, %s, %s)",
            (role_id, role.name, getattr(role, "description", None))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {
            "id": role_id,
            "name": role.name,
            "description": getattr(role, "description", None)
        }
    except Exception as e:
        print("❌ DB Error in add_role():", e)
        return {"error": str(e)}

# Get role by ID
def get_role_by_id(role_id):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, description, created_at FROM roles WHERE id=%s;", (str(role_id),))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return row
        return {"error": "Role not found"}
    except Exception as e:
        print("❌ DB Error in get_role_by_id():", e)
        return {"error": str(e)}

# Update role
def update_role(role_id, role):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE roles SET name=%s, description=%s WHERE id=%s",
            (role.name, getattr(role, "description", None), str(role_id))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        print("❌ DB Error in update_role():", e)
        return {"error": str(e)}

# Delete role
def delete_role(role_id):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM roles WHERE id=%s;", (str(role_id),))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        print("❌ DB Error in delete_role():", e)
        return {"error": str(e)}