import sqlite3
import os

db_path = r"E:\ML\database\database.db"
if os.path.exists(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT id, filepath FROM dataset_history")
    rows = cur.fetchall()
    print("Before update:")
    for r in rows:
        print(r)
    
    cur.execute("UPDATE dataset_history SET filepath = REPLACE(filepath, 'C:\\Users\\HP\\OneDrive\\Desktop\\ML', 'E:\\ML')")
    cur.execute("UPDATE dataset_history SET filepath = REPLACE(filepath, 'c:\\users\\hp\\onedrive\\desktop\\ml', 'E:\\ML')")
    cur.execute("UPDATE dataset_history SET filepath = REPLACE(filepath, 'C:/Users/HP/OneDrive/Desktop/ML', 'E:/ML')")
    con.commit()
    
    cur.execute("SELECT id, filepath FROM dataset_history")
    print("\nAfter update:")
    for r in cur.fetchall():
        print(r)
    con.close()
else:
    print(f"Database not found at {db_path}")
