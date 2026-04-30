from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.database.db import BASE_DIR, create_tables, get_connection


DATA_DIR = BASE_DIR / "app" / "data"


def read_json_file(file_path: Path) -> list[dict[str, Any]]:
    """
    Read a JSON file and return its content as a list of dictionaries.

    Args:
        file_path: Path to the JSON file.

    Returns:
        list[dict[str, Any]]: Parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the JSON content is invalid.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Missing data file: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in file: {file_path}") from exc

    if not isinstance(data, list):
        raise ValueError(f"Expected a list in JSON file: {file_path}")

    return data


def seed_users(users: list[dict[str, Any]]) -> None:
    """
    Insert or update users into the database.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.executemany(
            """
            INSERT OR REPLACE INTO users (
                user_id,
                name,
                preferred_cuisine,
                dietary_preference,
                budget_preference,
                default_location
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    user["user_id"],
                    user["name"],
                    user.get("preferred_cuisine"),
                    user.get("dietary_preference"),
                    user.get("budget_preference"),
                    user.get("default_location"),
                )
                for user in users
            ],
        )
        connection.commit()


def seed_restaurants(restaurants: list[dict[str, Any]]) -> None:
    """
    Insert or update restaurants into the database.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.executemany(
            """
            INSERT OR REPLACE INTO restaurants (
                restaurant_id,
                name,
                cuisine,
                location,
                is_halal,
                is_vegetarian_friendly,
                is_open,
                average_price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    restaurant["restaurant_id"],
                    restaurant["name"],
                    restaurant["cuisine"],
                    restaurant["location"],
                    int(restaurant["is_halal"]),
                    int(restaurant["is_vegetarian_friendly"]),
                    int(restaurant["is_open"]),
                    restaurant["average_price"],
                )
                for restaurant in restaurants
            ],
        )
        connection.commit()


def seed_menu_items(menu_items: list[dict[str, Any]]) -> None:
    """
    Insert or update menu items into the database.
    """
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.executemany(
            """
            INSERT OR REPLACE INTO menu_items (
                menu_id,
                restaurant_id,
                item_name,
                price,
                available,
                category
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["menu_id"],
                    item["restaurant_id"],
                    item["item_name"],
                    item["price"],
                    int(item["available"]),
                    item.get("category"),
                )
                for item in menu_items
            ],
        )
        connection.commit()


def show_table_counts() -> None:
    """
    Print row counts for the main database tables.
    """
    with get_connection() as connection:
        cursor = connection.cursor()

        for table_name in ["users", "restaurants", "menu_items", "orders", "notifications"]:
            cursor.execute(f"SELECT COUNT(*) AS count FROM {table_name}")
            count = cursor.fetchone()["count"]
            print(f"{table_name}: {count}")


def main() -> None:
    """
    Create database tables and load seed data from JSON files.
    """
    create_tables()

    users = read_json_file(DATA_DIR / "users.json")
    restaurants = read_json_file(DATA_DIR / "restaurants.json")
    menu_items = read_json_file(DATA_DIR / "menus.json")

    seed_users(users)
    seed_restaurants(restaurants)
    seed_menu_items(menu_items)

    print("Database initialized successfully.")
    show_table_counts()


if __name__ == "__main__":
    main()