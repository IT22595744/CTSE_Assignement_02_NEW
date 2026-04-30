from __future__ import annotations

import json
import uuid
from datetime import datetime, UTC
from typing import Any

from app.database.db import get_connection


def calculate_order_total(items: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Validate order items and calculate the total price.

    Expected item format:
        {"menu_id": "M001", "quantity": 2}

    Args:
        items: List of requested menu items with quantities.

    Returns:
        dict[str, Any]: Validated items and total price.

    Raises:
        ValueError: If the input is invalid.
        LookupError: If a menu item does not exist.
    """
    if not items:
        raise ValueError("items must not be empty.")

    validated_items: list[dict[str, Any]] = []
    total = 0.0

    with get_connection() as connection:
        cursor = connection.cursor()

        for item in items:
            menu_id = item.get("menu_id")
            quantity = item.get("quantity")

            if not menu_id or not isinstance(menu_id, str):
                raise ValueError("Each item must include a valid menu_id.")

            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError("Each item must include a positive integer quantity.")

            cursor.execute(
                """
                SELECT menu_id, restaurant_id, item_name, price, available, category
                FROM menu_items
                WHERE menu_id = ?
                """,
                (menu_id,),
            )
            row = cursor.fetchone()

            if row is None:
                raise LookupError(f"Menu item not found: {menu_id}")

            row_dict = dict(row)

            if row_dict["available"] != 1:
                raise ValueError(f"Menu item is currently unavailable: {menu_id}")

            line_total = float(row_dict["price"]) * quantity
            total += line_total

            validated_items.append(
                {
                    "menu_id": row_dict["menu_id"],
                    "restaurant_id": row_dict["restaurant_id"],
                    "item_name": row_dict["item_name"],
                    "unit_price": float(row_dict["price"]),
                    "quantity": quantity,
                    "line_total": line_total,
                    "category": row_dict["category"],
                }
            )

    return {
        "validated_items": validated_items,
        "total": round(total, 2),
        "currency": "LKR",
    }


def create_order_draft(
    user_id: str,
    restaurant_id: str,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Create a draft order in the database after validating items.

    Args:
        user_id: User placing the order.
        restaurant_id: Selected restaurant ID.
        items: List of items with menu_id and quantity.

    Returns:
        dict[str, Any]: Draft order data.

    Raises:
        ValueError: If data is invalid.
        LookupError: If the user or restaurant does not exist.
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id must not be empty.")

    if not restaurant_id or not restaurant_id.strip():
        raise ValueError("restaurant_id must not be empty.")

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id.strip(),))
        user_row = cursor.fetchone()
        if user_row is None:
            raise LookupError(f"User not found: {user_id}")

        cursor.execute(
            "SELECT restaurant_id, is_open FROM restaurants WHERE restaurant_id = ?",
            (restaurant_id.strip(),),
        )
        restaurant_row = cursor.fetchone()
        if restaurant_row is None:
            raise LookupError(f"Restaurant not found: {restaurant_id}")

        if restaurant_row["is_open"] != 1:
            raise ValueError(f"Restaurant is currently closed: {restaurant_id}")

    calculation = calculate_order_total(items)
    validated_items = calculation["validated_items"]

    item_restaurant_ids = {item["restaurant_id"] for item in validated_items}
    if item_restaurant_ids != {restaurant_id.strip()}:
        raise ValueError("All selected items must belong to the given restaurant_id.")

    order_id = f"O-{uuid.uuid4().hex[:8].upper()}"
    created_at = datetime.now(UTC).isoformat()
    total = calculation["total"]

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO orders (
                order_id, user_id, restaurant_id, items_json, total, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order_id,
                user_id.strip(),
                restaurant_id.strip(),
                json.dumps(validated_items, ensure_ascii=False),
                total,
                "DRAFT",
                created_at,
            ),
        )
        connection.commit()

    return {
        "order_id": order_id,
        "user_id": user_id.strip(),
        "restaurant_id": restaurant_id.strip(),
        "items": validated_items,
        "total": total,
        "currency": "LKR",
        "status": "DRAFT",
        "created_at": created_at,
    }