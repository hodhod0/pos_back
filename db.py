# db.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",         # XAMPP default
            database="pos_system",
            port=3306,
            auth_plugin="mysql_native_password"
        )
        return conn
    except Error as e:
        print("❌ MySQL connection error:", e)
        return None