import sqlite3
import json
import os

db_path = r"E:\ML\database\database.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables in DB:", tables)
    for t in tables:
        cursor.execute(f"SELECT count(*) FROM {t};")
        cnt = cursor.fetchone()[0]
        print(f"Table '{t}': {cnt} records")
        cursor.execute(f"PRAGMA table_info({t});")
        cols = [c[1] for c in cursor.fetchall()]
        print(f"  Columns: {cols}")
        cursor.execute(f"SELECT * FROM {t} ORDER BY rowid DESC LIMIT 3;")
        rows = cursor.fetchall()
        for r in rows:
            print("   Sample row:", r)
    conn.close()
else:
    print("DB not found at", db_path)

# Check reports and training files
for folder in [r"E:\ML\reports", r"E:\ML\report", r"E:\ML\models", r"E:\ML\training"]:
    if os.path.exists(folder):
        print(f"\nFiles in {folder}:", os.listdir(folder))
