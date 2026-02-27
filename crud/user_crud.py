from uuid import UUID

from db import get_connection

def get_all_users():
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ DB Error in get_all_users():", e)
        return {"error": str(e)}
