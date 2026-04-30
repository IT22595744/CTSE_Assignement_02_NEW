from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
env_db_path = os.getenv("DB_PATH", "app/database/smarteat.db")

if Path(env_db_path).is_absolute():
    DB_PATH = Path(env_db_path)
else:
    DB_PATH = (BASE_DIR / env_db_path).resolve()


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite connection.

    Returns:
        sqlite3.Connection: SQLite database connection with row access by column name.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables() -> None:
    """
    Create all required SmartEat MAS tables if they do not already exist.
    """
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                preferred_cuisine TEXT,
                dietary_preference TEXT,
                budget_preference REAL,
                default_location TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS restaurants (
                restaurant_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                cuisine TEXT NOT NULL,
                location TEXT NOT NULL,
                is_halal INTEGER NOT NULL,
                is_vegetarian_friendly INTEGER NOT NULL,
                is_open INTEGER NOT NULL,
                average_price REAL NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS menu_items (
                menu_id TEXT PRIMARY KEY,
                restaurant_id TEXT NOT NULL,
                item_name TEXT NOT NULL,
                price REAL NOT NULL,
                available INTEGER NOT NULL,
                category TEXT,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                restaurant_id TEXT NOT NULL,
                items_json TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()