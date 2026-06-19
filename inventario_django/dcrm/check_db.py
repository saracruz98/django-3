import sqlite3
import os

db_path = 'c:/Users/Lenovo/Downloads/liliana/inventario_django/dcrm/db.sqlite3'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM auth_user WHERE username='rawuser'")
    row = cursor.fetchone()
    print(f"User: {row[0]}, Password: {row[1]}")
    conn.close()
