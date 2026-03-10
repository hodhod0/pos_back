from uuid import UUID, uuid4
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
        item_id = item.id or uuid4()

        cursor.execute(
            "INSERT INTO items (id, name, price, category_id) VALUES (%s, %s, %s, %s)",
            (
                str(item_id),
                item.name,
                item.price,
                str(item.category_id) if item.category_id else None
            ),
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Item added successfully", "id": item_id}
    except Exception as e:
        print("❌ DB Error in add_item():", e)
        return {"error": str(e)}


def get_items_by_category(category_id: UUID):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor(dictionary=True)
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


def update_item(item):
    """
    Update an item by ID. Always returns success if item exists, even if values are unchanged.
    """
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor()

        # Ensure the item has an ID
        if not getattr(item, "id", None):
            return {"error": "Item ID is required for update"}

        cursor.execute(
            """
            UPDATE items
            SET name = %s,
                price = %s,
                category_id = %s
            WHERE id = %s
            """,
            (
                item.name,
                item.price,
                str(item.category_id) if item.category_id else None,
                str(item.id),
            ),
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Item updated successfully"}

    except Exception as e:
        print("❌ DB Error in update_item():", e)
        return {"error": str(e)}


def delete_item(item_id: UUID):
    conn = get_connection()
    if not conn:
        return {"error": "Cannot connect to database"}

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (str(item_id),))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return {"error": "Item not found"}
        return {"message": "Item deleted successfully"}
    except Exception as e:
        print("❌ DB Error in delete_item():", e)
        return {"error": str(e)}