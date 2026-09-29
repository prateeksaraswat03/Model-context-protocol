import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

DB_PATH = "spendly.db"

def get_db():
    """
    Opens connection to spendly.db in project root.
    Sets row_factory to sqlite3.Row and enables foreign keys.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates users and expenses tables if they don't exist.
    """
    with get_db() as conn:
        # Create users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Create expenses table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()

def seed_db():
    """
    Seeds the database with a demo user and sample expenses if empty.
    """
    with get_db() as conn:
        # Check if users table already contains data
        user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if user_count > 0:
            return

        # Insert demo user
        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash)
        )
        user_id = cursor.lastrowid

        # Define fixed categories
        categories = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]

        # Create 8 sample expenses
        sample_expenses = [
            (user_id, 15.50, "Food", (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), "Lunch at Deli"),
            (user_id, 42.00, "Transport", (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), "Gas refill"),
            (user_id, 120.00, "Bills", (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'), "Internet Bill"),
            (user_id, 60.00, "Health", (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'), "Pharmacy"),
            (user_id, 25.00, "Entertainment", (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), "Movie ticket"),
            (user_id, 89.99, "Shopping", (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'), "New shoes"),
            (user_id, 10.00, "Other", (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), "Parking fee"),
            (user_id, 30.00, "Food", (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d'), "Dinner with friends"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses
        )
        conn.commit()
