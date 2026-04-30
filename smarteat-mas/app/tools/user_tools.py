from __future__ import annotations

from typing import Any

from app.database.db import get_connection


def get_user_profile(user_id: str) -> dict[str, Any]:
    """
    Fetch a user profile from the database by user ID.

    Args:
        user_id: The unique user ID.

    Returns:
        dict[str, Any]: User profile information.

    Raises:
        ValueError: If user_id is empty.
        LookupError: If the user is not found.
    """
    if not user_id or not user_id.strip():
        raise ValueError("user_id must not be empty.")

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT user_id, name, preferred_cuisine, dietary_preference,
                   budget_preference, default_location
            FROM users
            WHERE user_id = ?
            """,
            (user_id.strip(),),
        )
        row = cursor.fetchone()

    if row is None:
        raise LookupError(f"User not found for user_id: {user_id}")

    return dict(row)