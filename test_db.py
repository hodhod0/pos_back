from db import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT *FROM item")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()