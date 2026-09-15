import sqlite3
import os

db = os.path.join(os.path.dirname(__file__), "expense.db")

with sqlite3.connect(db) as c:
    cur = c.execute(
        "INSERT INTO expenses(date,amount,category,subcategory,note) VALUES(?,?,?,?,?)",
        ("2026-08-31", 100, "Food", "", "Test")
    )
    print("Inserted ID:", cur.lastrowid)

    rows = c.execute("SELECT * FROM expenses").fetchall()
    print(rows)