from db import get_connection
from models.category import Category
import uuid
from fastapi import  HTTPException

# Get all categories
def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cat_id, cat_name FROM categories")
    rows = cursor.fetchall()
    conn.close()
    return [{"cat_id": str(r[0]), "cat_name": r[1]} for r in rows]

# Add a new category
def add_category(category: Category):
    conn = get_connection()
    cursor = conn.cursor()
    cat_id = uuid.uuid4()
    cursor.execute(
        "INSERT INTO categories (cat_id, cat_name) VALUES (%s, %s)",
        (str(cat_id), category.cat_name)
    )
    conn.commit()
    conn.close()
    return {"cat_id": str(cat_id), "message": "Category added"}

# Delete a category by ID
def delete_category(cat_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE cat_id = %s", (cat_id,))
    conn.commit()
    conn.close()
    return {"cat_id": cat_id, "message": "Category deleted"}

# Update (edit) a category by ID
def update_category(cat_id: str, category: Category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE categories SET cat_name = %s WHERE cat_id = %s",
        (category.cat_name, cat_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")

    conn.close()

    # ✅ RETURN UPDATED OBJECT
    return {
        "cat_id": cat_id,
        "cat_name": category.cat_name
    }
