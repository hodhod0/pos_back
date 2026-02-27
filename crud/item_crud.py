# crud/item_crud.py
from uuid import UUID

from db import get_connection

def get_all_items():
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ DB Error in get_all_items():", e)
        return {"error": str(e)}

def add_item(item):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, price, category_id) VALUES (%s, %s, %s)",
            (item.name, item.price, str(item.category_id))  # convert UUID to string
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Item added successfully"}
    except Exception as e:
        print("❌ DB Error in add_item():", e)
        return {"error": str(e)}
def get_items_by_category(category_id: UUID):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor(dictionary=True)
        # Convert UUID to string for MySQL
        cursor.execute(
            "SELECT * FROM items WHERE category_id = %s;", (str(category_id),)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ DB Error in get_items_by_category():", e)
        return {"error": str(e)}