from __future__ import annotations

from typing import Any

from app.database.db import get_connection


def search_restaurants(
    location: str | None = None,
    cuisine: str | None = None,
    halal: bool | None = None,
    vegetarian: bool | None = None,
    max_budget: float | None = None,
    only_open: bool = True,
) -> list[dict[str, Any]]:
    """
    Search restaurants using filters.

    Args:
        location: Preferred location.
        cuisine: Preferred cuisine.
        halal: Whether restaurant must be halal.
        vegetarian: Whether restaurant must be vegetarian-friendly.
        max_budget: Maximum average price allowed.
        only_open: Whether to return only currently open restaurants.

    Returns:
        list[dict[str, Any]]: Matching restaurant records.

    Raises:
        ValueError: If max_budget is invalid.
    """
    if max_budget is not None and max_budget < 0:
        raise ValueError("max_budget must be zero or greater.")

    query = """
        SELECT restaurant_id, name, cuisine, location, is_halal,
               is_vegetarian_friendly, is_open, average_price
        FROM restaurants
        WHERE 1 = 1
    """
    params: list[Any] = []

    if location:
        query += " AND LOWER(location) = LOWER(?)"
        params.append(location.strip())

    if cuisine:
        query += " AND LOWER(cuisine) = LOWER(?)"
        params.append(cuisine.strip())

    if halal is not None:
        query += " AND is_halal = ?"
        params.append(int(halal))

    if vegetarian is not None:
        query += " AND is_vegetarian_friendly = ?"
        params.append(int(vegetarian))

    if max_budget is not None:
        query += " AND average_price <= ?"
        params.append(max_budget)

    if only_open:
        query += " AND is_open = 1"

    query += " ORDER BY average_price ASC, name ASC"

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def get_restaurant_menu(
    restaurant_id: str,
    available_only: bool = True,
) -> list[dict[str, Any]]:
    """
    Retrieve menu items for a given restaurant.

    Args:
        restaurant_id: Restaurant identifier.
        available_only: Whether to include only available menu items.

    Returns:
        list[dict[str, Any]]: Menu item list.

    Raises:
        ValueError: If restaurant_id is empty.
    """
    if not restaurant_id or not restaurant_id.strip():
        raise ValueError("restaurant_id must not be empty.")

    query = """
        SELECT menu_id, restaurant_id, item_name, price, available, category
        FROM menu_items
        WHERE restaurant_id = ?
    """
    params: list[Any] = [restaurant_id.strip()]

    if available_only:
        query += " AND available = 1"

    query += " ORDER BY price ASC, item_name ASC"

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    return [dict(row) for row in rows]